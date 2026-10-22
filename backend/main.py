from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.api import (
    repository_router,
    search_router,
    chat_router,
    analysis_router,
    agent_router,
    settings_router,
)
from backend.api.state import app_state
from backend.utils.config import settings
from backend.utils.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AI Software Engineering Copilot Service...")
    app_state.initialize()
    yield
    # Shutdown
    logger.info("Shutting down AI Software Engineering Copilot Service...")

app = FastAPI(
    title="AI Software Engineering Copilot",
    description="Repository-Aware RAG-Based Intelligent Developer Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(repository_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(analysis_router)
app.include_router(agent_router)
app.include_router(settings_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
        "llm_model": settings.LLM_MODEL,
        "embedding_model": settings.EMBEDDING_MODEL,
        "indexed": app_state.index is not None,
    }

# Mount Frontend static assets
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    def serve_index():
        index_html = frontend_dir / "index.html"
        if index_html.exists():
            return FileResponse(index_html)
        return {"message": "AI Software Engineering Copilot API is running. Build frontend in frontend/index.html"}
