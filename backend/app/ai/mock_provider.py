import asyncio
from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage

class MockAiProvider(BaseAiProvider):
    @property
    def name(self) -> str:
        return "ISAI-MockProvider"

    async def generate_response(self, history: List[PromptMessage]) -> str:
        last_user_msg = next((m.content for m in reversed(history) if m.role == "user"), "Hello")
        return f"Hello! I am ISAI (Python FastAPI backend). You said: '{last_user_msg}'. How can I assist you today?"

    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        full_response = await self.generate_response(history)
        words = full_response.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.04)
