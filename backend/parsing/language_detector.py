from pathlib import Path
from typing import Optional, Dict

EXTENSION_TO_LANGUAGE: Dict[str, str] = {
    # Python
    ".py": "python",
    ".pyw": "python",
    ".pyx": "python",

    # JavaScript / TypeScript
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",

    # Java & JVM
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".scala": "scala",
    ".groovy": "groovy",

    # C / C++
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".hh": "cpp",

    # C# / .NET
    ".cs": "c_sharp",

    # Go & Rust
    ".go": "go",
    ".rs": "rust",

    # PHP
    ".php": "php",
    ".phtml": "php",

    # Ruby
    ".rb": "ruby",
    ".rake": "ruby",

    # Swift
    ".swift": "swift",

    # Dart
    ".dart": "dart",

    # Shell scripts
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".ps1": "powershell",

    # Lua & Perl
    ".lua": "lua",
    ".pl": "perl",
    ".pm": "perl",

    # R, Julia, Haskell, Elixir
    ".r": "r",
    ".R": "r",
    ".jl": "julia",
    ".hs": "haskell",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",

    # SQL
    ".sql": "sql",

    # Web & Config Markup
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "scss",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    ".md": "markdown",
}

class LanguageDetector:
    @staticmethod
    def detect_language(file_path: Path | str) -> Optional[str]:
        """Detect programming or config language from file extension."""
        suffix = Path(file_path).suffix.lower()
        return EXTENSION_TO_LANGUAGE.get(suffix)

    @staticmethod
    def is_supported(file_path: Path | str) -> bool:
        """Check if file has a known source or configuration extension."""
        return LanguageDetector.detect_language(file_path) is not None
