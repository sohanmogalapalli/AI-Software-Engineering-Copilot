import math
import re
from typing import Dict, List, Tuple
from collections import Counter
from backend.models.chunk import CodeChunk
from backend.ingestion.metadata import split_identifier

class BM25CodeStore:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.chunks: List[CodeChunk] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.doc_freqs: Dict[str, int] = {}  # term -> number of documents containing term
        self.doc_term_counts: List[Counter] = []

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize code text into lowercase keywords and split identifiers."""
        raw_words = re.findall(r"[a-zA-Z0-9_]+", text)
        tokens = []
        for word in raw_words:
            tokens.append(word.lower())
            tokens.extend(split_identifier(word))
        return [t for t in tokens if len(t) > 1]

    def build_index(self, chunks: List[CodeChunk]) -> None:
        """Index a list of code chunks."""
        self.chunks = chunks
        self.doc_lengths = []
        self.doc_term_counts = []
        self.doc_freqs = {}

        total_length = 0
        for chunk in chunks:
            # Index enriched content
            tokens = self.tokenize(chunk.enriched_content)
            doc_len = len(tokens)
            self.doc_lengths.append(doc_len)
            total_length += doc_len

            term_counts = Counter(tokens)
            self.doc_term_counts.append(term_counts)

            for term in term_counts:
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1

        n_docs = len(chunks)
        self.avg_doc_length = (total_length / n_docs) if n_docs > 0 else 1.0

    def search(self, query: str, top_k: int = 8) -> List[Tuple[CodeChunk, float]]:
        """Search chunks with BM25 Okapi."""
        if not self.chunks:
            return []

        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []

        n_docs = len(self.chunks)
        scores: List[float] = [0.0] * n_docs

        for token in query_tokens:
            if token not in self.doc_freqs:
                continue

            df = self.doc_freqs[token]
            # IDF formula with smoothing
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))

            for idx in range(n_docs):
                tf = self.doc_term_counts[idx][token]
                if tf > 0:
                    doc_len = self.doc_lengths[idx]
                    denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_length))
                    score = idf * (tf * (self.k1 + 1.0)) / denom
                    scores[idx] += score

        # Rank results
        ranked_indices = sorted(range(n_docs), key=lambda i: scores[i], reverse=True)
        results: List[Tuple[CodeChunk, float]] = []
        for idx in ranked_indices[:top_k]:
            if scores[idx] > 0.0:
                results.append((self.chunks[idx], scores[idx]))

        return results
