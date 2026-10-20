from backend.models.repository_index import RepositoryIndex
from backend.models.code_file import CodeFile
from backend.models.code_entity import CodeEntity
from backend.analysis.dependency_graph import DependencyGraphService
from backend.analysis.call_graph import CallGraphService
from backend.analysis.impact_analysis import ImpactAnalysisService

def build_mock_index():
    f1 = CodeFile(
        path="main.py", relative_path="main.py", language="python", content_hash="h1", line_count=20,
        imports=["auth"], entities=[CodeEntity(name="main_route", entity_type="function", file_path="main.py", start_line=1, end_line=10, source="pass", calls=["auth_user"])],
        all_calls=["auth_user"]
    )
    f2 = CodeFile(
        path="auth.py", relative_path="auth.py", language="python", content_hash="h2", line_count=30,
        imports=["db"], entities=[CodeEntity(name="auth_user", entity_type="function", file_path="auth.py", start_line=1, end_line=15, source="pass", calls=["query"])],
        all_calls=["query"]
    )
    f3 = CodeFile(
        path="db.py", relative_path="db.py", language="python", content_hash="h3", line_count=40,
        imports=[], entities=[CodeEntity(name="query", entity_type="function", file_path="db.py", start_line=1, end_line=20, source="pass")],
        all_calls=[]
    )

    index = RepositoryIndex(
        repository_path="/mock",
        name="mock_repo",
        indexed_at="2026-10-13",
        files={"main.py": f1, "auth.py": f2, "db.py": f3},
        languages={"python": 3},
        dependency_edges=[("main.py", "auth.py"), ("auth.py", "db.py")],
        call_edges=[("main.py", "auth.py"), ("auth.py", "db.py")]
    )
    return index

def test_dependency_graph():
    index = build_mock_index()
    dep_service = DependencyGraphService(index)
    
    assert dep_service.get_dependencies("main.py") == ["auth.py"]
    assert dep_service.get_dependents("db.py") == ["auth.py"]
    # Transitive dependents of db.py should include auth.py and main.py
    transitive = dep_service.get_transitive_dependents("db.py")
    assert "auth.py" in transitive
    assert "main.py" in transitive

def test_impact_analysis():
    index = build_mock_index()
    impact_service = ImpactAnalysisService(index)
    impact = impact_service.analyze_impact("db.py")

    assert impact["is_file"] is True
    assert "auth.py" in impact["all_affected_files"]
    assert "main.py" in impact["all_affected_files"]
    assert impact["risk_level"] in ("LOW", "MEDIUM", "HIGH")
