from typing import Optional
from backend.models.repository_index import RepositoryIndex
from backend.vectorstore.faiss_store import FAISSVectorStore
from backend.vectorstore.bm25_store import BM25CodeStore
from backend.vectorstore.retriever import HybridRetriever
from backend.embeddings.embedding_service import EmbeddingService
from backend.llm.ollama_client import OllamaClient
from backend.rag.rag_pipeline import RAGPipeline
from backend.rag.agent import CopilotAgent
from backend.utils.config import settings
from backend.utils.logging import logger

class AppState:
    index: Optional[RepositoryIndex] = None
    faiss_store: Optional[FAISSVectorStore] = None
    bm25_store: Optional[BM25CodeStore] = None
    embedding_service: Optional[EmbeddingService] = None
    llm_client: Optional[OllamaClient] = None
    retriever: Optional[HybridRetriever] = None
    rag_pipeline: Optional[RAGPipeline] = None
    agent: Optional[CopilotAgent] = None

    @classmethod
    def initialize(cls):
        """Initialize base models and attempt loading existing indexes from disk."""
        logger.info("Initializing Copilot AppState...")
        cls.embedding_service = EmbeddingService()
        cls.llm_client = OllamaClient()
        cls.faiss_store = FAISSVectorStore()
        cls.bm25_store = BM25CodeStore()

        # Try auto-loading existing vector store
        loaded = cls.faiss_store.load()
        if loaded:
            cls.bm25_store.build_index(cls.faiss_store.chunks)
            cls.retriever = HybridRetriever(cls.faiss_store, cls.bm25_store, cls.embedding_service)

            # Look for latest index json by modification time
            index_files = [f for f in settings.index_dir.glob("*_index.json") if f.is_file() and f.stat().st_size > 0]
            if index_files:
                latest_index = max(index_files, key=lambda f: f.stat().st_mtime)
                from backend.parsing.pipeline import ParsingPipeline
                p = ParsingPipeline()
                cls.index = p.load_index(latest_index)
                cls.rag_pipeline = RAGPipeline(cls.retriever, cls.llm_client, cls.index)
                cls.agent = CopilotAgent(cls.retriever, cls.llm_client, cls.index)
                logger.info(f"Loaded existing index for repository: {cls.index.name}")

    @classmethod
    def switch_to_repository(cls, repo_name: str) -> bool:
        """Dynamically switch repository context for per-chat isolation."""
        if not repo_name:
            return False
        clean_name = repo_name.strip()
        if cls.index and (cls.index.name == clean_name or cls.index.name.lower() == clean_name.lower()):
            return True

        idx_path = settings.index_dir / f"{clean_name}_index.json"
        if not idx_path.exists():
            candidates = list(settings.index_dir.glob(f"*{clean_name}*_index.json"))
            if candidates:
                idx_path = candidates[0]
                clean_name = idx_path.stem.replace("_index", "")
            else:
                logger.warning(f"Repository index '{clean_name}' not found on disk.")
                return False

        if cls.embedding_service is None:
            cls.embedding_service = EmbeddingService()
        if cls.llm_client is None:
            cls.llm_client = OllamaClient()
        if cls.faiss_store is None:
            cls.faiss_store = FAISSVectorStore()
        if cls.bm25_store is None:
            cls.bm25_store = BM25CodeStore()

        from backend.parsing.pipeline import ParsingPipeline
        p = ParsingPipeline()
        cls.index = p.load_index(idx_path)

        repo_vdir = settings.vector_store_dir / clean_name
        loaded = False
        if repo_vdir.exists() and (repo_vdir / "index.faiss").exists():
            loaded = cls.faiss_store.load(repo_vdir)
        if not loaded and (settings.vector_store_dir / "index.faiss").exists():
            cls.faiss_store.load(settings.vector_store_dir)

        cls.bm25_store.build_index(cls.faiss_store.chunks)
        cls.retriever = HybridRetriever(cls.faiss_store, cls.bm25_store, cls.embedding_service)
        cls.rag_pipeline = RAGPipeline(cls.retriever, cls.llm_client, cls.index)
        cls.agent = CopilotAgent(cls.retriever, cls.llm_client, cls.index)
        logger.info(f"Dynamically switched repository context to: {cls.index.name}")
        return True

app_state = AppState()
