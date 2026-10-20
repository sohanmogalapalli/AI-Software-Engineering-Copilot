from backend.models.code_file import CodeFile
from backend.models.code_entity import CodeEntity
from backend.ingestion.chunker import ContextEnrichedChunker
from backend.ingestion.metadata import split_identifier

def test_split_identifier():
    assert split_identifier("UserService") == ["user", "service"]
    assert split_identifier("get_user_by_id") == ["get", "user", "by", "id"]

def test_context_enriched_chunker():
    entity = CodeEntity(
        name="authenticate",
        entity_type="function",
        file_path="auth.py",
        start_line=10,
        end_line=20,
        source="def authenticate():\n    return True",
        docstring="Auth function"
    )
    code_file = CodeFile(
        path="auth.py",
        relative_path="auth.py",
        language="python",
        content_hash="abc123hash",
        line_count=20,
        imports=["jwt"],
        entities=[entity],
        all_calls=[]
    )

    chunks = ContextEnrichedChunker.chunk_file(code_file)
    assert len(chunks) == 2  # 1 overview + 1 entity
    entity_chunk = next(c for c in chunks if c.entity_name == "authenticate")
    assert "# File: auth.py" in entity_chunk.enriched_content
    assert "# Symbol: authenticate" in entity_chunk.enriched_content
    assert "def authenticate():" in entity_chunk.enriched_content
