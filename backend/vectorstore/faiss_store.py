import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import faiss
import numpy as np
from backend.models.chunk import CodeChunk
from backend.utils.config import settings
from backend.utils.logging import logger

class FAISSVectorStore:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        # IndexFlatIP calculates inner products. With normalized vectors, this equals cosine similarity.
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks: List[CodeChunk] = []

    @property
    def total_vectors(self) -> int:
        return self.index.ntotal

    def add_chunks(self, chunks: List[CodeChunk], vectors: np.ndarray) -> None:
        """Add chunks and their normalized embedding vectors to FAISS index."""
        if len(chunks) != len(vectors):
            raise ValueError(f"Mismatched chunks ({len(chunks)}) and vectors ({len(vectors)}) count")

        if len(vectors) == 0:
            return

        # Ensure float32 format
        v32 = np.ascontiguousarray(vectors, dtype=np.float32)
        self.index.add(v32)
        self.chunks.extend(chunks)
        logger.info(f"Added {len(chunks)} vectors to FAISS store. Total: {self.total_vectors}")

    def search(self, query_vector: np.ndarray, top_k: int = 8) -> List[Tuple[CodeChunk, float]]:
        """Search FAISS for nearest neighbors. Returns list of (chunk, similarity_score)."""
        if self.total_vectors == 0:
            return []

        q = np.ascontiguousarray(query_vector.reshape(1, -1), dtype=np.float32)
        scores, indices = self.index.search(q, min(top_k, self.total_vectors))

        results: List[Tuple[CodeChunk, float]] = []
        for idx, score in zip(indices[0], scores[0]):
            if idx >= 0 and idx < len(self.chunks):
                results.append((self.chunks[idx], float(score)))

        return results

    def save(self, directory: Optional[Path | str] = None) -> Path:
        """Save FAISS binary index and chunks metadata to disk."""
        target_dir = Path(directory) if directory else settings.vector_store_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        index_file = target_dir / "index.faiss"
        meta_file = target_dir / "metadata.json"

        faiss.write_index(self.index, str(index_file))

        with open(meta_file, "w", encoding="utf-8") as f:
            chunks_json = [c.model_dump() for c in self.chunks]
            json.dump(chunks_json, f, indent=2)

        logger.info(f"FAISS index and metadata saved to [green]{target_dir}[/green]")
        return target_dir

    def load(self, directory: Optional[Path | str] = None) -> bool:
        """Load FAISS index and chunks metadata from disk."""
        target_dir = Path(directory) if directory else settings.vector_store_dir
        index_file = target_dir / "index.faiss"
        meta_file = target_dir / "metadata.json"

        if not index_file.exists() or not meta_file.exists():
            logger.warning(f"No FAISS index found in {target_dir}")
            return False

        self.index = faiss.read_index(str(index_file))
        with open(meta_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.chunks = [CodeChunk.model_validate(item) for item in data]

        logger.info(f"Loaded FAISS store with {self.total_vectors} vectors from [green]{target_dir}[/green]")
        return True
