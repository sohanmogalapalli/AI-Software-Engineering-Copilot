import re
from typing import Dict, List, Optional, Tuple, Set
from backend.models.chunk import CodeChunk
from backend.embeddings.embedding_service import EmbeddingService
from backend.vectorstore.faiss_store import FAISSVectorStore
from backend.vectorstore.bm25_store import BM25CodeStore
from backend.utils.config import settings
from backend.utils.logging import logger

OVERVIEW_PATTERNS = [
    r"tell\s+me\s+full",
    r"about\s+(?:the\s+)?project",
    r"what\s+(?:is|does)\s+this",
    r"project\s+overview",
    r"architecture",
    r"how\s+does\s+it\s+work",
    r"what\s+is\s+neurovault",
    r"explain\s+(?:the\s+)?(repository|project|codebase)",
    r"tech\s+stack",
    r"features",
    r"summary"
]

class HybridRetriever:
    def __init__(
        self,
        vector_store: FAISSVectorStore,
        bm25_store: BM25CodeStore,
        embedding_service: EmbeddingService,
        rrf_k: int = 60
    ):
        self.vector_store = vector_store
        self.bm25_store = bm25_store
        self.embedding_service = embedding_service
        self.rrf_k = rrf_k

    def retrieve(
        self,
        query: str,
        top_k: int = 8,
        vector_weight: float = 1.0,
        bm25_weight: float = 1.0,
        symbol_boost: float = 1.5
    ) -> List[Tuple[CodeChunk, float, str]]:
        """
        Perform hybrid retrieval combining vector similarity, BM25 keyword matching,
        overview prioritization, and symbol matching using Reciprocal Rank Fusion (RRF).
        """
        clean_query = query.strip().lower()
        is_overview = any(re.search(pat, clean_query) for pat in OVERVIEW_PATTERNS)

        # 1. Vector Search
        query_vec = self.embedding_service.embed_text(query, normalize=True)
        vector_results = self.vector_store.search(query_vec, top_k=top_k * 4)

        # 2. BM25 Search
        bm25_results = self.bm25_store.search(query, top_k=top_k * 4)

        # 3. Exact Symbol & Overview Document Matches
        query_tokens = [t for t in re.findall(r"[a-zA-Z0-9_]+", clean_query) if len(t) > 2]
        symbol_matches: List[CodeChunk] = []

        # If overview query, prioritize README, PROJECT_OVERVIEW, main modules
        if is_overview:
            for chunk in self.vector_store.chunks:
                p_lower = chunk.relative_path.lower()
                if any(doc in p_lower for doc in ["overview.md", "readme.md", "architecture.md"]):
                    symbol_matches.append(chunk)
                elif "main.py" in p_lower or "app.py" in p_lower:
                    symbol_matches.append(chunk)

        # Match specific symbol names
        for chunk in self.vector_store.chunks:
            if chunk.entity_name and chunk.entity_name.lower() in query_tokens:
                symbol_matches.append(chunk)

        # Reciprocal Rank Fusion
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, CodeChunk] = {}
        provenance: Dict[str, List[str]] = {}

        # Dense ranking
        for rank, (chunk, score) in enumerate(vector_results, start=1):
            cid = chunk.chunk_id
            chunk_map[cid] = chunk
            provenance.setdefault(cid, []).append("dense")
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (vector_weight / (self.rrf_k + rank))

        # BM25 ranking
        for rank, (chunk, score) in enumerate(bm25_results, start=1):
            cid = chunk.chunk_id
            chunk_map[cid] = chunk
            provenance.setdefault(cid, []).append("bm25")
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (bm25_weight / (self.rrf_k + rank))

        # Overview / Symbol boost ranking
        for rank, chunk in enumerate(symbol_matches[:top_k * 3], start=1):
            cid = chunk.chunk_id
            chunk_map[cid] = chunk
            provenance.setdefault(cid, []).append("overview" if is_overview else "symbol")
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (symbol_boost / (self.rrf_k + rank))

        # Sort by total RRF score
        sorted_cids = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)

        # Diversity filter: don't let a single file take all top slots
        final_results: List[Tuple[CodeChunk, float, str]] = []
        file_counts: Dict[str, int] = {}

        for cid in sorted_cids:
            chunk = chunk_map[cid]
            fpath = chunk.relative_path
            count = file_counts.get(fpath, 0)
            if count >= 3:
                continue

            file_counts[fpath] = count + 1
            match_types = "+".join(provenance.get(cid, ["unknown"]))
            final_results.append((chunk, rrf_scores[cid], match_types))

            if len(final_results) >= top_k:
                break

        logger.info(f"Hybrid retrieval for '{query}' returned {len(final_results)} chunks (is_overview={is_overview}).")
        return final_results
