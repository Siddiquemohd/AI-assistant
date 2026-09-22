from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage
from app.ai.mock_provider import MockAiProvider
from app.ai.ollama_provider import OllamaProvider
from app.ai.openai_provider import OpenAiProvider
from app.core.config import settings

class AiGateway:
    def __init__(self):
        self._mock_provider = MockAiProvider()
        self._ollama_provider = OllamaProvider()
        self._openai_provider = OpenAiProvider()

    def get_provider(self, mode: str = "auto") -> BaseAiProvider:
        if mode == "local":
            return self._ollama_provider
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip():
            return self._openai_provider
        # Default fallback to mock provider if no API key is configured
        return self._mock_provider

    async def generate_response(self, history: List[PromptMessage], mode: str = "auto") -> str:
        provider = self.get_provider(mode)
        try:
            return await provider.generate_response(history)
        except Exception:
            # Fallback to mock provider on error
            return await self._mock_provider.generate_response(history)

    async def stream_response(self, history: List[PromptMessage], mode: str = "auto") -> AsyncGenerator[str, None]:
        provider = self.get_provider(mode)
        try:
            async for chunk in provider.stream_response(history):
                yield chunk
        except Exception:
            async for chunk in self._mock_provider.stream_response(history):
                yield chunk
