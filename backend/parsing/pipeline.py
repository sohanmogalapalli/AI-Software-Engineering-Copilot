import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from backend.models.code_file import CodeFile
from backend.models.repository_index import RepositoryIndex
from backend.parsing.repository_scanner import RepositoryScanner
from backend.parsing.tree_sitter_parser import TreeSitterManager
from backend.parsing.entity_extractor import EntityExtractor
from backend.parsing.import_extractor import ImportExtractor
from backend.parsing.call_extractor import CallExtractor
from backend.utils.file_utils import normalize_path, read_file_content
from backend.utils.logging import logger
from backend.utils.config import settings

class ParsingPipeline:
    def __init__(self):
        self.scanner = RepositoryScanner()
        self.ts_manager = TreeSitterManager()

    def process_repository(self, repo_path: Path | str) -> RepositoryIndex:
        """Parse repository and build a complete structural RepositoryIndex."""
        root_path = Path(repo_path).resolve()
        repo_name = root_path.name
        start_time = datetime.now(timezone.utc).isoformat()

        discovered = self.scanner.scan(root_path)
        files_dict: Dict[str, CodeFile] = {}
        language_counts: Dict[str, int] = {}
        all_entities_by_name: Dict[str, List[str]] = {}  # symbol_name -> list of relative file paths

        logger.info(f"Parsing ASTs for {len(discovered)} files...")

        for file_path, language, file_hash in discovered:
            rel_path = normalize_path(file_path.relative_to(root_path))
            content = read_file_content(file_path)
            if content is None:
                continue

            language_counts[language] = language_counts.get(language, 0) + 1
            line_count = len(content.splitlines())

            tree = self.ts_manager.parse(content, language)
            if not tree:
                # Add file as unparsed container
                code_file = CodeFile(
                    path=normalize_path(file_path),
                    relative_path=rel_path,
                    language=language,
                    content_hash=file_hash,
                    line_count=line_count,
                    imports=[],
                    entities=[],
                    all_calls=[]
                )
                files_dict[rel_path] = code_file
                continue

            root_node = tree.root_node
            imports = ImportExtractor.extract_imports(root_node, content, language)
            entities = EntityExtractor.extract_entities(root_node, content, rel_path, language)
            all_calls = CallExtractor.extract_calls(root_node, content, language)

            for ent in entities:
                all_entities_by_name.setdefault(ent.name, []).append(rel_path)
                if ent.parent_entity:
                    all_entities_by_name.setdefault(f"{ent.parent_entity}.{ent.name}", []).append(rel_path)

            code_file = CodeFile(
                path=normalize_path(file_path),
                relative_path=rel_path,
                language=language,
                content_hash=file_hash,
                line_count=line_count,
                imports=imports,
                entities=entities,
                all_calls=all_calls
            )
            files_dict[rel_path] = code_file

        # Build Dependency and Call Edges
        dependency_edges: List[Tuple[str, str]] = []
        call_edges: List[Tuple[str, str]] = []

        all_rel_paths = list(files_dict.keys())

        for rel_path, code_file in files_dict.items():
            # Match imports to other files in repository
            for imp in code_file.imports:
                imp_parts = imp.replace(".", "/").split("/")
                for target_rel in all_rel_paths:
                    if target_rel != rel_path:
                        target_without_ext = str(Path(target_rel).with_suffix(""))
                        if any(target_without_ext.endswith(part) for part in imp_parts if len(part) > 2):
                            edge = (rel_path, target_rel)
                            if edge not in dependency_edges:
                                dependency_edges.append(edge)

            # Match calls to entities defined in other files
            for call_name in code_file.all_calls:
                clean_name = call_name.split(".")[-1]
                if clean_name in all_entities_by_name:
                    for target_file in all_entities_by_name[clean_name]:
                        if target_file != rel_path:
                            edge = (rel_path, target_file)
                            if edge not in call_edges:
                                call_edges.append(edge)

        index = RepositoryIndex(
            repository_path=normalize_path(root_path),
            name=repo_name,
            indexed_at=start_time,
            files=files_dict,
            languages=language_counts,
            dependency_edges=dependency_edges,
            call_edges=call_edges
        )

        logger.info(
            f"Repository indexed: {index.total_files} files, {index.total_entities} entities, "
            f"{len(dependency_edges)} dependency edges, {len(call_edges)} call edges."
        )
        return index

    def save_index(self, index: RepositoryIndex, save_path: Optional[Path | str] = None) -> Path:
        """Persist RepositoryIndex to JSON disk file."""
        if save_path is None:
            settings.index_dir.mkdir(parents=True, exist_ok=True)
            save_path = settings.index_dir / f"{index.name}_index.json"
        
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(index.model_dump_json(indent=2))
        logger.info(f"Index saved to [green]{path}[/green]")
        return path

    def load_index(self, load_path: Path | str) -> RepositoryIndex:
        """Load RepositoryIndex from JSON disk file."""
        path = Path(load_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return RepositoryIndex.model_validate(data)
