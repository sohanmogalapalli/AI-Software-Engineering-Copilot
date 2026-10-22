import time
from typing import List, Optional
import numpy as np
import httpx
import ollama
from backend.utils.config import settings
from backend.utils.logging import logger

MAX_EMBED_CHARS = 4000
GOOGLE_EMBED_MODEL = "gemini-embedding-001"
TARGET_DIMENSION = 768

class EmbeddingService:
    """
    High-performance embedding service with:
    1. Fast Batched Google Cloud Embeddings (gemini-embedding-001 @ 768 dims)
    2. Fallback to Local Ollama (nomic-embed-text)
    """
    def __init__(self, model_name: Optional[str] = None, base_url: Optional[str] = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self._ollama_client = ollama.Client(host=self.base_url)
        self.dimension = TARGET_DIMENSION
        self.base_gemini_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def _get_gemini_key(self) -> Optional[str]:
        return settings.GEMINI_API_KEY

    def _embed_text_gemini(self, text: str, key: str, normalize: bool = True) -> np.ndarray:
        url = f"{self.base_gemini_url}/{GOOGLE_EMBED_MODEL}:embedContent?key={key}"
        safe_text = text[:MAX_EMBED_CHARS]
        payload = {
            "model": f"models/{GOOGLE_EMBED_MODEL}",
            "content": {"parts": [{"text": safe_text}]},
            "outputDimensionality": TARGET_DIMENSION
        }
        for attempt in range(3):
            try:
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        vals = resp.json().get("embedding", {}).get("values", [])
                        if vals:
                            vec = np.array(vals, dtype=np.float32)
                            if normalize:
                                norm = np.linalg.norm(vec)
                                if norm > 0:
                                    vec = vec / norm
                            return vec
                    elif resp.status_code == 429:
                        time.sleep(1.0 * (attempt + 1))
                        continue
                    else:
                        logger.warning(f"Gemini single embed failed ({resp.status_code}): {resp.text[:100]}")
                        break
            except Exception as e:
                if attempt == 2:
                    logger.warning(f"Gemini embed exception: {e}")
                time.sleep(0.5 * (attempt + 1))
        return np.zeros(self.dimension, dtype=np.float32)

    def _embed_batch_gemini(self, texts: List[str], key: str, batch_size: int = 50, normalize: bool = True) -> np.ndarray:
        total = len(texts)
        logger.info(f"⚡ Generating fast cloud embeddings for {total} chunks via Google Gemini ({GOOGLE_EMBED_MODEL})...")
        url = f"{self.base_gemini_url}/{GOOGLE_EMBED_MODEL}:batchEmbedContents?key={key}"
        all_vectors = []

        with httpx.Client(timeout=45.0) as client:
            for i in range(0, total, batch_size):
                batch = texts[i : i + batch_size]
                requests = [
                    {
                        "model": f"models/{GOOGLE_EMBED_MODEL}",
                        "content": {"parts": [{"text": t[:MAX_EMBED_CHARS]}]},
                        "outputDimensionality": TARGET_DIMENSION
                    }
                    for t in batch
                ]
                payload = {"requests": requests}
                success = False

                for attempt in range(3):
                    try:
                        resp = client.post(url, json=payload)
                        if resp.status_code == 200:
                            data = resp.json()
                            embs = data.get("embeddings", [])
                            for emb in embs:
                                vals = emb.get("values", [])
                                if vals:
                                    vec = np.array(vals, dtype=np.float32)
                                    if normalize:
                                        norm = np.linalg.norm(vec)
                                        if norm > 0:
                                            vec = vec / norm
                                    all_vectors.append(vec)
                                else:
                                    all_vectors.append(np.zeros(self.dimension, dtype=np.float32))
                            success = True
                            break
                        elif resp.status_code == 429:
                            time.sleep(1.5 * (attempt + 1))
                        else:
                            logger.warning(f"Batch embed status {resp.status_code}: {resp.text[:120]}")
                            time.sleep(1.0)
                    except Exception as e:
                        time.sleep(1.0 * (attempt + 1))

                if not success:
                    # Fallback single embedding for this batch
                    logger.warning(f"Batch failed, falling back to per-chunk embedding for batch {i}..{i+len(batch)}")
                    for t in batch:
                        vec = self._embed_text_gemini(t, key, normalize=normalize)
                        all_vectors.append(vec)

                progress = min(total, i + len(batch))
                logger.info(f"⚡ Progress: {progress} / {total} embeddings generated in cloud.")

        return np.vstack(all_vectors).astype(np.float32)

    def _embed_text_ollama(self, text: str, normalize: bool = True) -> np.ndarray:
        safe_text = text[:MAX_EMBED_CHARS] if len(text) > MAX_EMBED_CHARS else text
        for attempt in range(3):
            try:
                res = self._ollama_client.embeddings(model=self.model_name, prompt=safe_text, keep_alive="24h")
                vec = np.array(res["embedding"], dtype=np.float32)
                if normalize:
                    norm = np.linalg.norm(vec)
                    if norm > 0:
                        vec = vec / norm
                return vec
            except Exception as e:
                err_str = str(e).lower()
                if "context length" in err_str or "length exceeds" in err_str or "500" in err_str:
                    safe_text = safe_text[: max(500, len(safe_text) // 2)]
                    continue
                if attempt == 2:
                    logger.warning(f"Could not embed chunk with Ollama: {e}. Using zero vector fallback.")
                    return np.zeros(self.dimension, dtype=np.float32)
                time.sleep(0.5 * (attempt + 1))
        return np.zeros(self.dimension, dtype=np.float32)

    def embed_text(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Generate embedding vector for a single query text string.
        Uses Google Cloud if key is configured, else falls back to local Ollama.
        """
        gemini_key = self._get_gemini_key()
        if gemini_key:
            try:
                return self._embed_text_gemini(text, gemini_key, normalize=normalize)
            except Exception as e:
                logger.warning(f"Gemini single embed failed, falling back to Ollama: {e}")

        return self._embed_text_ollama(text, normalize=normalize)

    def embed_batch(self, texts: List[str], batch_size: int = 50, normalize: bool = True) -> np.ndarray:
        """
        Generate embeddings for a batch of text chunks.
        Uses ultra-fast Google Cloud batching if key is available, else local Ollama.
        """
        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)

        gemini_key = self._get_gemini_key()
        if gemini_key:
            try:
                return self._embed_batch_gemini(texts, gemini_key, batch_size=batch_size, normalize=normalize)
            except Exception as e:
                logger.warning(f"Gemini batch embedding error, falling back to Ollama: {e}")

        # Local Ollama Fallback
        vectors = []
        total = len(texts)
        logger.info(f"Generating embeddings for {total} chunks using Ollama ({self.model_name})...")

        for i in range(0, total, 16):
            batch = texts[i : i + 16]
            for text in batch:
                vec = self._embed_text_ollama(text, normalize=normalize)
                vectors.append(vec)
            if (i + len(batch)) % 50 == 0 or (i + len(batch)) == total:
                logger.info(f"Progress: {i + len(batch)} / {total} embeddings generated.")

        return np.vstack(vectors).astype(np.float32)
