from typing import Dict, Optional
from tree_sitter import Language, Parser
from backend.utils.logging import logger

class TreeSitterManager:
    _instance: Optional["TreeSitterManager"] = None
    _parsers: Dict[str, Parser] = {}

    def __new__(cls) -> "TreeSitterManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_parsers()
        return cls._instance

    def _init_parsers(self) -> None:
        """Initialize available tree-sitter language parsers with fallback."""
        loaders = {
            "python": ("tree_sitter_python", "language"),
            "javascript": ("tree_sitter_javascript", "language"),
            "typescript": ("tree_sitter_typescript", "language_typescript"),
            "java": ("tree_sitter_java", "language"),
            "cpp": ("tree_sitter_cpp", "language"),
            "c": ("tree_sitter_c", "language"),
            "c_sharp": ("tree_sitter_c_sharp", "language"),
            "csharp": ("tree_sitter_c_sharp", "language"),
            "go": ("tree_sitter_go", "language"),
            "rust": ("tree_sitter_rust", "language"),
            "kotlin": ("tree_sitter_kotlin", "language"),
            "php": ("tree_sitter_php", "language_php"),
        }

        for lang_name, (pkg_name, attr_name) in loaders.items():
            try:
                mod = __import__(pkg_name)
                func = getattr(mod, attr_name, None) or getattr(mod, "language", None)
                if func:
                    lang = Language(func())
                    parser = Parser(lang)
                    self._parsers[lang_name] = parser
            except Exception as e:
                logger.debug(f"Could not load tree-sitter parser for {lang_name}: {e}")

    def get_parser(self, language: str) -> Optional[Parser]:
        return self._parsers.get(language.lower())

    def parse(self, source_code: str, language: str):
        parser = self.get_parser(language)
        if not parser:
            return None
        source_bytes = source_code.encode("utf-8", errors="replace")
        try:
            return parser.parse(source_bytes)
        except Exception as e:
            logger.debug(f"Tree-sitter parse error for {language}: {e}")
            return None
