import json
import httpx
from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage
from app.core.config import settings

class OpenAiProvider(BaseAiProvider):
    @property
    def name(self) -> str:
        return f"OpenAI-{settings.OPENAI_MODEL}"

    async def generate_response(self, history: List[PromptMessage]) -> str:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        messages = [{"role": m.role, "content": m.content} for m in history]

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": messages,
            "temperature": 0.7
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.OPENAI_BASE_URL.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        messages = [{"role": m.role, "content": m.content} for m in history]

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "stream": True
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                f"{settings.OPENAI_BASE_URL.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk_json = json.loads(data_str)
                            delta = chunk_json["choices"][0]["delta"]
                            content = delta.get("content")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
