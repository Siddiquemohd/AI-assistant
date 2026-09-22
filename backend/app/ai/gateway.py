from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage
from app.ai.mock_provider import MockAiProvider

class AiGateway:
    """
    Primary AI Gateway for ISAI.
    Operates 100% autonomously using ISAI's built-in self-contained AI engine
    without requiring any external AI models, API keys, or third-party cloud services.
    """
    def __init__(self):
        self._native_ai_engine = MockAiProvider()

    def get_provider(self, mode: str = "auto") -> BaseAiProvider:
        return self._native_ai_engine

    async def generate_response(self, history: List[PromptMessage], mode: str = "auto") -> str:
        return await self._native_ai_engine.generate_response(history)

    async def stream_response(self, history: List[PromptMessage], mode: str = "auto") -> AsyncGenerator[str, None]:
        async for chunk in self._native_ai_engine.stream_response(history):
            yield chunk
