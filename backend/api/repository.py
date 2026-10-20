from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from backend.api.state import app_state
from backend.parsing.pipeline import ParsingPipeline
from backend.ingestion.pipeline import IngestionPipeline
from backend.vectorstore.retriever import HybridRetriever
from backend.rag.rag_pipeline import RAGPipeline
from backend.rag.agent import CopilotAgent
from backend.utils.config import settings
from backend.utils.logging import logger

from backend.parsing.github_cloner import GitHubCloner

router = APIRouter(prefix="/api/repository", tags=["repository"])

class IndexRepoRequest(BaseModel):
    repository_path: str = Field(description="Local path to repository folder")
    force_reindex: bool = Field(default=False, description="Whether to rebuild from scratch")

class CloneRepoRequest(BaseModel):
    github_url: str = Field(description="GitHub repository URL (e.g. https://github.com/owner/repo)")
    branch: Optional[str] = Field(default=None, description="Optional branch or tag to clone")
    force: bool = Field(default=False, description="Whether to re-clone if directory already exists")

def ensure_app_state_initialized():
    if app_state.embedding_service is None:
        from backend.embeddings.embedding_service import EmbeddingService
        app_state.embedding_service = EmbeddingService()
    if app_state.faiss_store is None:
        from backend.vectorstore.faiss_store import FAISSVectorStore
        app_state.faiss_store = FAISSVectorStore(app_state.embedding_service.dimension)
    if app_state.bm25_store is None:
        from backend.vectorstore.bm25_store import BM25CodeStore
        app_state.bm25_store = BM25CodeStore()
    if app_state.llm_client is None:
        from backend.llm.ollama_client import OllamaClient
        app_state.llm_client = OllamaClient()

def _run_indexing_job(repo_path: str):
    root_path = Path(repo_path).resolve()
    logger.info(f"Starting full indexing pipeline for: {root_path}")
    ensure_app_state_initialized()

    # 1. Parsing
    parser = ParsingPipeline()
    index = parser.process_repository(root_path)
    parser.save_index(index)
    app_state.index = index

    # 2. Ingestion & Chunking
    chunks = IngestionPipeline.ingest(index)
    IngestionPipeline.save_chunks(chunks, index.name)

    # 3. Embedding & FAISS Store
    texts_to_embed = [c.enriched_content for c in chunks]
    vectors = app_state.embedding_service.embed_batch(texts_to_embed)

    app_state.faiss_store.chunks.clear()
    import faiss
    app_state.faiss_store.index = faiss.IndexFlatIP(app_state.embedding_service.dimension)
    app_state.faiss_store.add_chunks(chunks, vectors)
    app_state.faiss_store.save()
    # Save dedicated copy for this repo
    repo_vdir = settings.vector_store_dir / index.name
    app_state.faiss_store.save(repo_vdir)

    # 4. BM25 & Hybrid Retriever
    app_state.bm25_store.build_index(chunks)
    app_state.retriever = HybridRetriever(app_state.faiss_store, app_state.bm25_store, app_state.embedding_service)

    # 5. RAG Pipeline & Agent
    app_state.rag_pipeline = RAGPipeline(app_state.retriever, app_state.llm_client, app_state.index)
    app_state.agent = CopilotAgent(app_state.retriever, app_state.llm_client, app_state.index)

    logger.info(f"Indexing completed successfully for {index.name}!")

@router.post("/index")
def index_repository(request: IndexRepoRequest, background_tasks: BackgroundTasks):
    path = Path(request.repository_path).resolve()
    if not path.exists():
        raise HTTPException(status_code=400, detail=f"Path not found: {path}")

    # Run synchronously if repository is small, or schedule in background
    _run_indexing_job(str(path))
    return {
        "status": "success",
        "message": f"Repository '{path.name}' indexed successfully.",
        "path": str(path),
        "total_files": app_state.index.total_files if app_state.index else 0,
        "total_entities": app_state.index.total_entities if app_state.index else 0,
        "total_chunks": len(app_state.faiss_store.chunks) if app_state.faiss_store else 0,
    }

@router.post("/clone")
def clone_and_index_github_repo(request: CloneRepoRequest):
    try:
        dest_path = GitHubCloner.clone_repository(
            github_url=request.github_url,
            branch=request.branch,
            force=request.force
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to clone GitHub repository: {e}")

    try:
        _run_indexing_job(str(dest_path))
    except Exception as e:
        logger.error(f"Failed to index cloned repository: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to index cloned repository: {e}")
    return {
        "status": "success",
        "message": f"GitHub repository '{dest_path.name}' cloned and indexed successfully.",
        "path": str(dest_path),
        "github_url": request.github_url,
        "total_files": app_state.index.total_files if app_state.index else 0,
        "total_entities": app_state.index.total_entities if app_state.index else 0,
        "total_chunks": len(app_state.faiss_store.chunks) if app_state.faiss_store else 0,
    }

@router.get("/status")
def get_repository_status():
    if not app_state.index:
        return {
            "indexed": False,
            "message": "No repository has been indexed yet."
        }

    return {
        "indexed": True,
        "repository_name": app_state.index.name,
        "repository_path": app_state.index.repository_path,
        "indexed_at": app_state.index.indexed_at,
        "total_files": app_state.index.total_files,
        "total_entities": app_state.index.total_entities,
        "total_vectors": app_state.faiss_store.total_vectors if app_state.faiss_store else 0,
        "languages": app_state.index.languages,
        "dependency_edges_count": len(app_state.index.dependency_edges),
        "call_edges_count": len(app_state.index.call_edges),
    }

@router.get("/files")
def list_indexed_files():
    if not app_state.index:
        return {"files": []}

    files = []
    for rel_path, cf in app_state.index.files.items():
        files.append({
            "path": rel_path,
            "language": cf.language,
            "lines": cf.line_count,
            "classes": len(cf.classes),
            "functions": len(cf.functions),
            "imports": len(cf.imports)
        })
    return {"files": files}

class SwitchRepoRequest(BaseModel):
    repository_name: str = Field(description="Name of the repository to switch active context to")

@router.get("/list")
def list_repositories():
    """List all indexed repositories available for exploration."""
    repos = []
    active_name = app_state.index.name if app_state.index else None
    
    import json
    for idx_file in settings.index_dir.glob("*_index.json"):
        if idx_file.is_file() and idx_file.stat().st_size > 0:
            name = idx_file.stem.replace("_index", "")
            try:
                with open(idx_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    repos.append({
                        "name": name,
                        "display_name": data.get("name", name),
                        "path": data.get("repository_path", ""),
                        "total_files": data.get("total_files", 0),
                        "total_entities": data.get("total_entities", 0),
                        "languages": data.get("languages", []),
                        "is_active": (name == active_name or data.get("name") == active_name)
                    })
            except Exception as e:
                logger.error(f"Error reading index file {idx_file}: {e}")
                
    return {"repositories": repos, "active_repository": active_name}

@router.post("/switch")
def switch_repository(request: SwitchRepoRequest):
    """Switch the active codebase context dynamically for multi-repo chats."""
    repo_name = request.repository_name.strip()
    idx_path = settings.index_dir / f"{repo_name}_index.json"
    if not idx_path.exists():
        candidates = list(settings.index_dir.glob(f"*{repo_name}*_index.json"))
        if candidates:
            idx_path = candidates[0]
            repo_name = idx_path.stem.replace("_index", "")
        else:
            raise HTTPException(status_code=404, detail=f"Repository index '{repo_name}' not found.")

    ensure_app_state_initialized()
    from backend.parsing.pipeline import ParsingPipeline
    p = ParsingPipeline()
    index = p.load_index(idx_path)
    app_state.index = index

    # Try dedicated repo vector store dir first
    repo_vdir = settings.vector_store_dir / repo_name
    loaded = False
    if repo_vdir.exists() and (repo_vdir / "index.faiss").exists():
        loaded = app_state.faiss_store.load(repo_vdir)

    if not loaded:
        if (settings.vector_store_dir / "index.faiss").exists():
            app_state.faiss_store.load(settings.vector_store_dir)

    # Rebuild BM25 & retriever
    app_state.bm25_store.build_index(app_state.faiss_store.chunks)
    app_state.retriever = HybridRetriever(app_state.faiss_store, app_state.bm25_store, app_state.embedding_service)
    app_state.rag_pipeline = RAGPipeline(app_state.retriever, app_state.llm_client, app_state.index)
    app_state.agent = CopilotAgent(app_state.retriever, app_state.llm_client, app_state.index)

    logger.info(f"Switched active codebase context to: {index.name}")
    return {
        "status": "success",
        "message": f"Successfully switched to codebase '{index.name}'.",
        "repository_name": index.name,
        "total_files": index.total_files,
        "total_chunks": len(app_state.faiss_store.chunks)
    }
