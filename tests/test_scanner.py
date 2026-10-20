from pathlib import Path
from backend.parsing.language_detector import LanguageDetector
from backend.parsing.repository_scanner import RepositoryScanner

def test_language_detection():
    assert LanguageDetector.detect_language("main.py") == "python"
    assert LanguageDetector.detect_language("app.ts") == "typescript"
    assert LanguageDetector.detect_language("index.js") == "javascript"
    assert LanguageDetector.detect_language("Main.java") == "java"
    assert LanguageDetector.detect_language("unknown.xyz") is None

def test_repository_scanner(tmp_path: Path):
    # Create sample files
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "test.py").write_text("def hello(): pass")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "ignored.js").write_text("console.log('ignore');")

    scanner = RepositoryScanner()
    discovered = scanner.scan(tmp_path)

    paths = [p[0].name for p in discovered]
    assert "test.py" in paths
    assert "ignored.js" not in paths
