from typing import Generator, Optional
from backend.utils.config import settings
from backend.utils.logging import logger
from backend.llm.ollama_client import OllamaClient
from backend.llm.gemini_client import GeminiClient
from backend.llm.openai_compatible_client import OpenAICompatibleClient

class UnifiedLLMClient:
    """
    Unified LLM router that dynamically directs inference requests to:
    1. Google Gemini (Free tier, ultra-fast sub-second cloud inference)
    2. Groq Cloud (Free tier, 300-500 tokens/sec LPU)
    3. xAI Grok (grok-2, grok-beta)
    4. Local Ollama (fallback for offline/local private execution)
    """
    def __init__(self):
        self.ollama = OllamaClient()
        self.gemini = GeminiClient(default_model="gemini-3-flash-preview")
        self.groq = OpenAICompatibleClient(
            base_url="https://api.groq.com/openai/v1",
            default_model="openai/gpt-oss-120b",
            provider_name="groq"
        )
        self.grok = OpenAICompatibleClient(
            base_url="https://api.x.ai/v1",
            default_model="grok-2-mini",
            provider_name="grok"
        )

    def detect_provider(self, model: Optional[str] = None, provider: Optional[str] = None) -> str:
        """Resolve the target LLM provider based on explicit choice, model name, or configured keys."""
        if provider:
            p = provider.strip().lower()
            if p in ["gemini", "google"]:
                return "gemini"
            if p in ["grok", "xai"]:
                return "grok"
            if p in ["groq"]:
                return "groq"
            if p in ["ollama", "local"]:
                return "ollama"

        m = (model or "").lower().strip()
        if "gemini" in m:
            return "gemini"
        if "grok" in m:
            return "grok"
        if "groq" in m or "oss" in m or "llama" in m:
            return "groq"
        if ":" in m:  # e.g. qwen2.5-coder:7b
            return "ollama"

        # Check configured runtime API keys in order of speed & quality
        if settings.GEMINI_API_KEY:
            return "gemini"
        if settings.GROQ_API_KEY:
            return "groq"
        if settings.GROK_API_KEY:
            return "grok"

        if settings.LLM_PROVIDER and settings.LLM_PROVIDER != "auto":
            return settings.LLM_PROVIDER

        return "gemini"

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> str:
        target_provider = self.detect_provider(model=model, provider=provider)
        target_model = model or settings.LLM_MODEL

        try:
            if target_provider == "gemini":
                gemini_model = target_model if "gemini" in target_model else "gemini-3-flash-preview"
                return self.gemini.generate(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=gemini_model,
                    api_key=api_key
                )
            elif target_provider == "groq":
                groq_model = target_model if "oss" in target_model else "openai/gpt-oss-120b"
                return self.groq.generate(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=groq_model,
                    api_key=api_key
                )
            elif target_provider == "grok":
                grok_model = target_model if "grok" in target_model else "grok-2-mini"
                return self.grok.generate(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=grok_model,
                    api_key=api_key
                )
            else:
                return self.ollama.generate(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=target_model
                )
        except Exception as e:
            logger.error(f"Error generating with provider {target_provider}: {e}")
            raise e

    def stream_generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Generator[str, None, None]:
        target_provider = self.detect_provider(model=model, provider=provider)
        target_model = model or settings.LLM_MODEL

        if target_provider == "gemini":
            gemini_model = target_model if "gemini" in target_model else "gemini-3-flash-preview"
            yield from self.gemini.stream_generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                model=gemini_model,
                api_key=api_key
            )
        elif target_provider == "groq":
            groq_model = target_model if "oss" in target_model else "openai/gpt-oss-120b"
            yield from self.groq.stream_generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                model=groq_model,
                api_key=api_key
            )
        elif target_provider == "grok":
            grok_model = target_model if "grok" in target_model else "grok-2-mini"
            yield from self.grok.stream_generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                model=grok_model,
                api_key=api_key
            )
        else:
            try:
                yield from self.ollama.stream_generate(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=target_model
                )
            except Exception as e:
                logger.error(f"Error streaming with Ollama: {e}")
                yield (
                    f"\n[Could not connect to local Ollama ({e}). "
                    "For instant sub-second answers without local GPU load, switch to Google Gemini (Free) or Groq in Settings.]"
                )
