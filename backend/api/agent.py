from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.api.state import app_state

router = APIRouter(prefix="/api/agent", tags=["agent"])

class AgentRequest(BaseModel):
    query: str = Field(description="Complex query requiring multi-step investigation")
    max_steps: int = Field(default=2, description="Maximum number of reasoning tool-use steps")
    repository: Optional[str] = Field(default=None, description="Target repository for this chat")
    model: Optional[str] = Field(default=None, description="Optional LLM model override")
    provider: Optional[str] = Field(default=None, description="Optional provider override")
    api_key: Optional[str] = Field(default=None, description="Optional API key override")

@router.post("/run")
def run_agent(request: AgentRequest):
    if request.repository:
        app_state.switch_to_repository(request.repository)

    if not app_state.agent:
        raise HTTPException(status_code=400, detail="Repository not indexed yet.")

    result = app_state.agent.run(
        request.query,
        max_steps=request.max_steps,
        model=request.model,
        provider=request.provider,
        api_key=request.api_key
    )
    return result
