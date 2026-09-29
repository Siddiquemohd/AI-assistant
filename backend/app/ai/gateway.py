from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage
from app.ai.huggingface_provider import HuggingFaceProvider

class AiGateway:
    """
    Primary AI Gateway for ISAI.
    Operates 100% autonomously using custom fine-tuned Llama-3.2-3B model on Hugging Face.
    """
    def __init__(self):
        self._native_ai_engine = HuggingFaceProvider(repo_id="Siddiquiee/ISAI-Custom-Llama3.2-3B")

    def get_provider(self, mode: str = "auto") -> BaseAiProvider:
        return self._native_ai_engine

    async def generate_response(self, history: List[PromptMessage], mode: str = "auto") -> str:
        return await self._native_ai_engine.generate_response(history)

    async def stream_response(self, history: List[PromptMessage], mode: str = "auto") -> AsyncGenerator[str, None]:
        async for chunk in self._native_ai_engine.stream_response(history):
            yield chunk
