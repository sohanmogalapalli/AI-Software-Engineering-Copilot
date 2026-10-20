from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.api.state import app_state

router = APIRouter(prefix="/api/search", tags=["search"])

class SearchRequest(BaseModel):
    query: str = Field(description="Search query string or code snippet")
    top_k: int = Field(default=8, description="Number of top results to return")

@router.post("")
def search_code(request: SearchRequest):
    if not app_state.retriever:
        raise HTTPException(status_code=400, detail="Repository must be indexed before searching.")

    results = app_state.retriever.retrieve(request.query, top_k=request.top_k)
    items = []
    for chunk, score, prov in results:
        items.append({
            "chunk_id": chunk.chunk_id,
            "file": chunk.relative_path,
            "language": chunk.language,
            "entity_name": chunk.entity_name,
            "entity_type": chunk.entity_type,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "content": chunk.content,
            "score": round(score, 4),
            "match_provenance": prov,
            "imports": chunk.imports[:5],
            "calls": chunk.calls[:5],
        })

    return {
        "query": request.query,
        "total_results": len(items),
        "results": items
    }
