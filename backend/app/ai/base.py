from abc import ABC, abstractmethod
from typing import AsyncGenerator, List
from pydantic import BaseModel

class PromptMessage(BaseModel):
    role: str
    content: str

class BaseAiProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def generate_response(self, history: List[PromptMessage]) -> str:
        pass

    @abstractmethod
    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        pass
