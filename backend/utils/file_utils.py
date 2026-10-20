import hashlib
from pathlib import Path
from typing import List, Optional, Set

DEFAULT_IGNORE_DIRS: Set[str] = {
    ".git", ".svn", ".hg", "__pycache__", ".venv", "venv", "env",
    "node_modules", "dist", "build", ".next", ".nuxt", "target",
    ".idea", ".vscode", ".pytest_cache", ".mypy_cache", "coverage",
    "site-packages", ".tox"
}

def get_content_hash(content: str) -> str:
    """Compute SHA-256 hash of a string."""
    return hashlib.sha256(content.encode("utf-8", errors="replace")).hexdigest()

def get_file_hash(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def read_file_content(file_path: Path) -> Optional[str]:
    """Read file content with UTF-8 fallback to latin-1."""
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding="latin-1")
        except Exception:
            return None
    except Exception:
        return None

def normalize_path(path: Path | str) -> str:
    """Return POSIX-style relative or normalized path string."""
    return str(Path(path).as_posix())
