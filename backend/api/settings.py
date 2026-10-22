import os
import time
from typing import Optional, List, Dict, Any
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import httpx

from backend.utils.config import settings, PROJECT_ROOT
from backend.utils.logging import logger
from backend.llm.unified_client import UnifiedLLMClient

router = APIRouter(prefix="/api/settings", tags=["settings"])

class SettingsUpdateRequest(BaseModel):
    gemini_api_key: Optional[str] = Field(default=None)
    grok_api_key: Optional[str] = Field(default=None)
    groq_api_key: Optional[str] = Field(default=None)
    provider: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)

class TestConnectionRequest(BaseModel):
    provider: str = Field(description="Target provider (gemini, groq, grok, ollama)")
    model: Optional[str] = Field(default=None)
    api_key: Optional[str] = Field(default=None)

def mask_key(key: Optional[str]) -> Optional[str]:
    if not key or len(key) < 8:
        return None
    return f"{key[:4]}...{key[-4:]}"

def update_env_file(key_values: Dict[str, str]):
    env_path = PROJECT_ROOT / ".env"
    existing_lines = []
    if env_path.exists():
        existing_lines = env_path.read_text(encoding="utf-8").splitlines()

    parsed = {}
    other_lines = []
    for line in existing_lines:
        line_s = line.strip()
        if line_s and not line_s.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            parsed[k.strip()] = v.strip()
        else:
            other_lines.append(line)

    for k, v in key_values.items():
        if v is not None:
            parsed[k] = v

    # Write back
    out = []
    for line in existing_lines:
        if "=" in line and not line.strip().startswith("#"):
            k = line.split("=", 1)[0].strip()
            if k in parsed:
                out.append(f"{k}={parsed.pop(k)}")
            else:
                out.append(line)
        else:
            out.append(line)
    for k, v in parsed.items():
        out.append(f"{k}={v}")

    env_path.write_text("\n".join(out) + "\n", encoding="utf-8")

@router.get("")
def get_settings():
    # Test local Ollama availability quickly (500ms timeout)
    ollama_ok = False
    try:
        resp = httpx.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=0.5)
        ollama_ok = resp.status_code == 200
    except Exception:
        ollama_ok = False

    return {
        "active_provider": settings.LLM_PROVIDER,
        "active_model": settings.LLM_MODEL,
        "gemini": {
            "configured": bool(settings.GEMINI_API_KEY),
            "masked": mask_key(settings.GEMINI_API_KEY),
        },
        "grok": {
            "configured": bool(settings.GROK_API_KEY),
            "masked": mask_key(settings.GROK_API_KEY),
        },
        "groq": {
            "configured": bool(settings.GROQ_API_KEY),
            "masked": mask_key(settings.GROQ_API_KEY),
        },
        "ollama": {
            "available": ollama_ok,
            "base_url": settings.OLLAMA_BASE_URL,
        },
        "recommended_models": [
            {
                "id": "gemini-3-flash-preview",
                "name": "⚡ Google Gemini 3 Flash (Verified • Free Tier)",
                "provider": "gemini",
                "speed": "< 0.8s",
                "category": "cloud_free",
                "description": "Latest ultra-fast Google AI model with generous free tier. Massive context.",
                "badge": "⚡ Sub-Second"
            },
            {
                "id": "gemini-3.1-flash-lite-preview",
                "name": "⚡ Google Gemini 3.1 Flash-Lite (Free Tier)",
                "provider": "gemini",
                "speed": "< 0.6s",
                "category": "cloud_free",
                "description": "Instant lightweight reasoning model with minimal latency.",
                "badge": "⚡ Instant"
            },
            {
                "id": "openai/gpt-oss-120b",
                "name": "🚀 Groq GPT-OSS 120B (Free Tier)",
                "provider": "groq",
                "speed": "< 0.8s",
                "category": "cloud_free",
                "description": "High parameter reasoning model powered by ultra-fast Groq LPU inference.",
                "badge": "🚀 300+ tok/s"
            },
            {
                "id": "openai/gpt-oss-20b",
                "name": "🚀 Groq GPT-OSS 20B (Free Tier)",
                "provider": "groq",
                "speed": "< 0.5s",
                "category": "cloud_free",
                "description": "Ultra-fast compact code analysis model on Groq.",
                "badge": "🚀 Instant"
            },
            {
                "id": "grok-2-mini",
                "name": "🤖 xAI Grok-2 Mini",
                "provider": "grok",
                "speed": "1-2s",
                "category": "cloud",
                "description": "xAI's compact fast reasoning model.",
                "badge": "🤖 Grok"
            },
            {
                "id": "qwen2.5-coder:3b",
                "name": "💻 Qwen2.5-Coder 3B (Local Ollama)",
                "provider": "ollama",
                "speed": "5-15s",
                "category": "local",
                "description": "Lightweight local code model for offline use.",
                "badge": "💻 Local"
            },
            {
                "id": "qwen2.5-coder:7b",
                "name": "🧠 Qwen2.5-Coder 7B (Local Ollama)",
                "provider": "ollama",
                "speed": "15-60s",
                "category": "local",
                "description": "Full local coding model. High VRAM/CPU intensive.",
                "badge": "🧠 Deep Local"
            }
        ]
    }

@router.post("")
def update_settings(req: SettingsUpdateRequest):
    updates = {}
    if req.gemini_api_key is not None:
        key = req.gemini_api_key.strip()
        settings.GEMINI_API_KEY = key if key else None
        updates["GEMINI_API_KEY"] = key

    if req.grok_api_key is not None:
        key = req.grok_api_key.strip()
        settings.GROK_API_KEY = key if key else None
        updates["GROK_API_KEY"] = key

    if req.groq_api_key is not None:
        key = req.groq_api_key.strip()
        settings.GROQ_API_KEY = key if key else None
        updates["GROQ_API_KEY"] = key

    if req.provider:
        settings.LLM_PROVIDER = req.provider.strip()
        updates["LLM_PROVIDER"] = req.provider.strip()

    if req.model:
        settings.LLM_MODEL = req.model.strip()
        updates["LLM_MODEL"] = req.model.strip()

    if updates:
        try:
            update_env_file(updates)
        except Exception as e:
            logger.warning(f"Could not persist settings to .env: {e}")

    return {
        "status": "success",
        "active_provider": settings.LLM_PROVIDER,
        "active_model": settings.LLM_MODEL,
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "grok_configured": bool(settings.GROK_API_KEY),
        "groq_configured": bool(settings.GROQ_API_KEY),
    }

@router.post("/test")
def test_connection(req: TestConnectionRequest):
    client = UnifiedLLMClient()
    start_t = time.time()
    try:
        reply = client.generate(
            prompt="Reply with the single word 'OK'.",
            system="You are a speed test probe. Answer with only 'OK'.",
            temperature=0.0,
            max_tokens=10,
            model=req.model,
            provider=req.provider,
            api_key=req.api_key
        )
        elapsed_ms = int((time.time() - start_t) * 1000)
        return {
            "success": True,
            "provider": req.provider,
            "model": req.model,
            "latency_ms": elapsed_ms,
            "reply": reply.strip(),
            "message": f"Successfully connected! Latency: {elapsed_ms}ms"
        }
    except Exception as e:
        elapsed_ms = int((time.time() - start_t) * 1000)
        return {
            "success": False,
            "provider": req.provider,
            "model": req.model,
            "latency_ms": elapsed_ms,
            "error": str(e),
            "message": f"Connection failed ({elapsed_ms}ms): {e}"
        }
