import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.parsing.pipeline import ParsingPipeline
from backend.ingestion.pipeline import IngestionPipeline
from backend.embeddings.embedding_service import EmbeddingService
from backend.vectorstore.faiss_store import FAISSVectorStore
from backend.vectorstore.bm25_store import BM25CodeStore
from backend.vectorstore.retriever import HybridRetriever
from backend.utils.logging import logger

from backend.parsing.github_cloner import GitHubCloner

def main():
    parser = argparse.ArgumentParser(description="Index a repository for the AI Copilot")
    parser.add_argument("repo_path", nargs="?", default=str(PROJECT_ROOT), help="Path to repository directory or GitHub URL")
    parser.add_argument("--branch", default=None, help="Optional branch name if cloning from GitHub")
    parser.add_argument("--force", action="store_true", help="Force re-clone if already exists")
    args = parser.parse_args()

    raw_path = args.repo_path.strip()
    if raw_path.startswith("http://") or raw_path.startswith("https://") or raw_path.startswith("git@"):
        logger.info(f"Detected GitHub URL: [cyan]{raw_path}[/cyan]. Cloning...")
        repo_dir = GitHubCloner.clone_repository(raw_path, branch=args.branch, force=args.force)
    else:
        repo_dir = Path(raw_path).resolve()
        
    logger.info(f"Indexing repository at: [cyan]{repo_dir}[/cyan]")

    # 1. Parse AST
    pipeline = ParsingPipeline()
    index = pipeline.process_repository(repo_dir)
    pipeline.save_index(index)

    # 2. Ingest & Chunk
    chunks = IngestionPipeline.ingest(index)
    IngestionPipeline.save_chunks(chunks, index.name)

    # 3. Embed & Vector Store
    embedder = EmbeddingService()
    texts = [c.enriched_content for c in chunks]
    vectors = embedder.embed_batch(texts)

    faiss_store = FAISSVectorStore(embedder.dimension)
    faiss_store.add_chunks(chunks, vectors)
    faiss_store.save()

    logger.info(f"[green]Successfully indexed '{index.name}' with {len(chunks)} chunks and vectors.[/green]")

if __name__ == "__main__":
    main()
