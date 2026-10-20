import os
from pathlib import Path
from typing import List, Set, Tuple
from backend.utils.file_utils import DEFAULT_IGNORE_DIRS, get_file_hash, normalize_path
from backend.parsing.language_detector import LanguageDetector
from backend.utils.logging import logger

class RepositoryScanner:
    def __init__(self, ignore_dirs: Set[str] | None = None):
        self.ignore_dirs = set(ignore_dirs) if ignore_dirs else set(DEFAULT_IGNORE_DIRS)

    def scan(self, repo_path: Path | str) -> List[Tuple[Path, str, str]]:
        """
        Scan repository directory for supported source files.
        Returns List of tuples: (absolute_file_path, language, file_sha256_hash)
        """
        root = Path(repo_path).resolve()
        if not root.exists():
            raise FileNotFoundError(f"Repository path does not exist: {root}")

        discovered_files: List[Tuple[Path, str, str]] = []
        logger.info(f"Scanning repository: [cyan]{root}[/cyan]")

        for dirpath, dirnames, filenames in os.walk(root):
            # Prune ignored directories in-place
            dirnames[:] = [d for d in dirnames if d not in self.ignore_dirs and not d.startswith(".")]

            for filename in filenames:
                file_path = Path(dirpath) / filename
                lang = LanguageDetector.detect_language(file_path)
                if lang:
                    try:
                        file_hash = get_file_hash(file_path)
                        discovered_files.append((file_path, lang, file_hash))
                    except Exception as e:
                        logger.warning(f"Could not read {file_path}: {e}")

        logger.info(f"Discovered {len(discovered_files)} supported source files.")
        return discovered_files
