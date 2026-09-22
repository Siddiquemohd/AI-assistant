import httpx
from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage
from app.core.config import settings

class OllamaProvider(BaseAiProvider):
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.base_url = settings.OLLAMA_BASE_URL

    @property
    def name(self) -> str:
        return f"Ollama-{self.model_name}"

    async def generate_response(self, history: List[PromptMessage]) -> str:
        messages = [{"role": m.role, "content": m.content} for m in history]
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False
                }
            )
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"]

    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        messages = [{"role": m.role, "content": m.content} for m in history]
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": True
                }
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        # Parse chunk data if needed
                        yield data_str
