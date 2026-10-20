import numpy as np
from backend.models.chunk import CodeChunk
from backend.vectorstore.bm25_store import BM25CodeStore
from backend.vectorstore.faiss_store import FAISSVectorStore

def test_bm25_search():
    c1 = CodeChunk(
        chunk_id="1", file_path="auth.py", relative_path="auth.py", language="python",
        entity_name="login", entity_type="function", start_line=1, end_line=10,
        content="def login(): return True", enriched_content="# File: auth.py\ndef login(): return True",
        imports=[], calls=[]
    )
    c2 = CodeChunk(
        chunk_id="2", file_path="db.py", relative_path="db.py", language="python",
        entity_name="connect", entity_type="function", start_line=1, end_line=10,
        content="def connect(): pass", enriched_content="# File: db.py\ndef connect(): pass",
        imports=[], calls=[]
    )

    bm25 = BM25CodeStore()
    bm25.build_index([c1, c2])

    results = bm25.search("login function")
    assert len(results) > 0
    assert results[0][0].chunk_id == "1"

def test_faiss_vector_store():
    d = 768
    store = FAISSVectorStore(dimension=d)
    c = CodeChunk(
        chunk_id="c1", file_path="test.py", relative_path="test.py", language="python",
        entity_name="test", entity_type="function", start_line=1, end_line=5,
        content="pass", enriched_content="pass", imports=[], calls=[]
    )
    vec = np.ones((1, d), dtype=np.float32)
    vec = vec / np.linalg.norm(vec)

    store.add_chunks([c], vec)
    assert store.total_vectors == 1

    res = store.search(vec[0], top_k=1)
    assert len(res) == 1
    assert res[0][0].chunk_id == "c1"
    assert abs(res[0][1] - 1.0) < 1e-4
