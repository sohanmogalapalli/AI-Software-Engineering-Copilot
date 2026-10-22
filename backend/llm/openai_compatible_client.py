import json
from typing import Generator, Optional
import httpx
from backend.utils.config import settings
from backend.utils.logging import logger

GROQ_DEFAULT_MODEL = "openai/gpt-oss-120b"

GROQ_MODEL_ALIASES = {
    "llama-3.1-8b-instant": "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile": "openai/gpt-oss-120b",
    "gpt-oss-120b": "openai/gpt-oss-120b",
    "gpt-oss-20b": "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b": "openai/gpt-oss-120b",
}

class OpenAICompatibleClient:
    """
    Client for OpenAI-compatible inference APIs, including:
    - Groq Cloud (Free tier LPU - 300-500 tokens/sec)
    - xAI Grok (Grok-2, Grok-beta)
    - OpenAI / OpenRouter
    """
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        default_model: str = "openai/gpt-oss-120b",
        provider_name: str = "groq"
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.default_model = default_model
        self.provider_name = provider_name

    def _get_api_key(self, api_key_override: Optional[str] = None) -> str:
        key = api_key_override or self.api_key
        if not key:
            if self.provider_name == "groq":
                key = settings.GROQ_API_KEY
            elif self.provider_name == "grok":
                key = settings.GROK_API_KEY
        if not key:
            raise ValueError(
                f"{self.provider_name.upper()} API key is missing. Please configure it in Settings or .env file."
            )
        return key

    def _resolve_model(self, model: Optional[str]) -> str:
        target = model or self.default_model
        if self.provider_name == "groq":
            return GROQ_MODEL_ALIASES.get(target, target)
        return target

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> str:
        key = self._get_api_key(api_key)
        target_model = self._resolve_model(model)
        endpoint = f"{self.base_url}/chat/completions"

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

        with httpx.Client(timeout=60.0) as client:
            resp = client.post(endpoint, json=payload, headers=headers)
            if resp.status_code == 404 and self.provider_name == "groq" and target_model != GROQ_DEFAULT_MODEL:
                logger.warning(f"Groq model {target_model} returned 404, falling back to {GROQ_DEFAULT_MODEL}")
                payload["model"] = GROQ_DEFAULT_MODEL
                resp = client.post(endpoint, json=payload, headers=headers)

            if resp.status_code != 200:
                try:
                    err = resp.json().get("error", {}).get("message", resp.text)
                except Exception:
                    err = resp.text
                logger.error(f"{self.provider_name} API error ({resp.status_code}): {err}")
                raise RuntimeError(f"{self.provider_name} API error ({resp.status_code}): {err}")

            data = resp.json()
            return data["choices"][0]["message"]["content"]

    def _stream_from_endpoint(self, client: httpx.Client, endpoint: str, payload: dict, headers: dict) -> Generator[str, None, None]:
        with client.stream("POST", endpoint, json=payload, headers=headers) as response:
            if response.status_code == 404 and self.provider_name == "groq":
                raise FileNotFoundError("Model not found (404)")

            if response.status_code != 200:
                content = response.read().decode("utf-8", errors="replace")
                try:
                    err_msg = json.loads(content).get("error", {}).get("message", content)
                except Exception:
                    err_msg = content
                yield f"\n[{self.provider_name.upper()} API error ({response.status_code}): {err_msg}]"
                return

            for line in response.iter_lines():
                if not line:
                    continue
                if line.startswith("data: "):
                    data_str = line[6:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        choices = chunk.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            content = delta.get("content")
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        pass

    def stream_generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Generator[str, None, None]:
        try:
            key = self._get_api_key(api_key)
        except Exception as e:
            yield f"\n[Configuration Error: {e}]"
            return

        target_model = self._resolve_model(model)
        endpoint = f"{self.base_url}/chat/completions"

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                try:
                    yield from self._stream_from_endpoint(client, endpoint, payload, headers)
                except FileNotFoundError:
                    logger.warning(f"Groq model {target_model} returned 404, falling back to {GROQ_DEFAULT_MODEL}")
                    payload["model"] = GROQ_DEFAULT_MODEL
                    yield from self._stream_from_endpoint(client, endpoint, payload, headers)
        except Exception as e:
            logger.error(f"Streaming error with {self.provider_name}: {e}")
            yield f"\n[{self.provider_name.upper()} streaming error: {e}]"
