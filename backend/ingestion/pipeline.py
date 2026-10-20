import json
from pathlib import Path
from typing import List, Optional
from backend.models.chunk import CodeChunk
from backend.models.repository_index import RepositoryIndex
from backend.ingestion.chunker import ContextEnrichedChunker
from backend.utils.config import settings
from backend.utils.logging import logger

class IngestionPipeline:
    @staticmethod
    def ingest(index: RepositoryIndex) -> List[CodeChunk]:
        """Convert RepositoryIndex into enriched chunks."""
        return ContextEnrichedChunker.chunk_repository(index)

    @staticmethod
    def save_chunks(chunks: List[CodeChunk], repo_name: str, save_path: Optional[Path | str] = None) -> Path:
        """Save chunk list to JSON file."""
        if save_path is None:
            settings.chunk_dir.mkdir(parents=True, exist_ok=True)
            save_path = settings.chunk_dir / f"{repo_name}_chunks.json"

        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        chunks_data = [chunk.model_dump() for chunk in chunks]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunks_data, f, indent=2)
        logger.info(f"Saved {len(chunks)} chunks to [green]{path}[/green]")
        return path

    @staticmethod
    def load_chunks(load_path: Path | str) -> List[CodeChunk]:
        """Load chunks from JSON file."""
        path = Path(load_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [CodeChunk.model_validate(item) for item in data]
