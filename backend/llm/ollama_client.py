from typing import AsyncGenerator, Dict, Generator, List, Optional
import ollama
from backend.utils.config import settings
from backend.utils.logging import logger

class OllamaClient:
    def __init__(self, model_name: Optional[str] = None, base_url: Optional[str] = None):
        self.model_name = model_name or settings.LLM_MODEL
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self._client = ollama.Client(host=self.base_url)

    def generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 512, model: Optional[str] = None) -> str:
        """Synchronous text generation."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        target_model = model or self.model_name
        try:
            res = self._client.chat(
                model=target_model,
                messages=messages,
                keep_alive="24h",
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "num_ctx": 2048,
                }
            )
            return res["message"]["content"]
        except Exception as e:
            logger.error(f"Error calling Ollama model {target_model}: {e}")
            raise e

    def stream_generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 512, model: Optional[str] = None) -> Generator[str, None, None]:
        """Synchronous streaming token generator."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        target_model = model or self.model_name
        try:
            stream = self._client.chat(
                model=target_model,
                messages=messages,
                stream=True,
                keep_alive="24h",
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "num_ctx": 2048,
                }
            )
            for chunk in stream:
                token = chunk["message"]["content"]
                yield token
        except Exception as e:
            logger.error(f"Streaming error with Ollama {target_model}: {e}")
            yield f"\n[Error communicating with local LLM: {e}]"
