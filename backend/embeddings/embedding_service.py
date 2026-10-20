import time
from typing import List, Optional
import numpy as np
import ollama
from backend.utils.config import settings
from backend.utils.logging import logger

MAX_EMBED_CHARS = 4000  # Safe character limit for nomic-embed-text (2048 tokens)

class EmbeddingService:
    def __init__(self, model_name: Optional[str] = None, base_url: Optional[str] = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self._client = ollama.Client(host=self.base_url)
        self.dimension = 768  # Standard for nomic-embed-text

    def embed_text(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Generate embedding vector for a single text string.
        Safely bounds text length to prevent exceeding embedding model context length.
        """
        safe_text = text[:MAX_EMBED_CHARS] if len(text) > MAX_EMBED_CHARS else text

        for attempt in range(3):
            try:
                res = self._client.embeddings(model=self.model_name, prompt=safe_text, keep_alive="24h")
                vec = np.array(res["embedding"], dtype=np.float32)
                if normalize:
                    norm = np.linalg.norm(vec)
                    if norm > 0:
                        vec = vec / norm
                return vec
            except Exception as e:
                err_str = str(e).lower()
                if "context length" in err_str or "length exceeds" in err_str or "500" in err_str:
                    # Dynamically halve text length and retry immediately
                    safe_text = safe_text[: max(500, len(safe_text) // 2)]
                    continue

                if attempt == 2:
                    logger.warning(f"Could not embed chunk snippet: {e}. Using zero vector fallback.")
                    return np.zeros(self.dimension, dtype=np.float32)

                time.sleep(0.5 * (attempt + 1))

        return np.zeros(self.dimension, dtype=np.float32)

    def embed_batch(self, texts: List[str], batch_size: int = 16, normalize: bool = True) -> np.ndarray:
        """Generate embeddings for a batch of text strings."""
        vectors = []
        total = len(texts)
        logger.info(f"Generating embeddings for {total} chunks using {self.model_name}...")

        for i in range(0, total, batch_size):
            batch = texts[i : i + batch_size]
            for text in batch:
                vec = self.embed_text(text, normalize=normalize)
                vectors.append(vec)
            if (i + len(batch)) % 50 == 0 or (i + len(batch)) == total:
                logger.info(f"Progress: {i + len(batch)} / {total} embeddings generated.")

        return np.vstack(vectors).astype(np.float32)
