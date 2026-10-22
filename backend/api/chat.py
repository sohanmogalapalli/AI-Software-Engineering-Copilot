import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from backend.api.state import app_state

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    query: str = Field(description="Developer question or request")
    top_k: int = Field(default=5, description="Number of context chunks to retrieve")
    repository: Optional[str] = Field(default=None, description="Target repository for this chat")
    model: Optional[str] = Field(default=None, description="Optional LLM model override")
    provider: Optional[str] = Field(default=None, description="Optional LLM provider override (gemini, groq, grok, ollama)")
    api_key: Optional[str] = Field(default=None, description="Optional API key override")

@router.post("")
def chat_with_copilot(request: ChatRequest):
    if request.repository:
        app_state.switch_to_repository(request.repository)

    if not app_state.rag_pipeline:
        raise HTTPException(status_code=400, detail="Repository must be indexed before starting chat.")

    response = app_state.rag_pipeline.query(
        request.query,
        top_k=request.top_k,
        model=request.model,
        provider=request.provider,
        api_key=request.api_key
    )
    return response

@router.post("/stream")
def chat_stream(request: ChatRequest):
    if request.repository:
        app_state.switch_to_repository(request.repository)

    if not app_state.rag_pipeline:
        raise HTTPException(status_code=400, detail="Repository must be indexed before starting chat.")

    def event_stream():
        for event in app_state.rag_pipeline.stream_query(
            request.query,
            top_k=request.top_k,
            model=request.model,
            provider=request.provider,
            api_key=request.api_key
        ):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
