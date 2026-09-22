from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.other import Memory
from app.schemas.memory import MemoryCreateRequest, MemoryUpdateRequest, MemoryDto

class MemoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_memories(self, user_id: str) -> List[MemoryDto]:
        stmt = select(Memory).where(Memory.user_id == user_id, Memory.deleted_at == None).order_by(Memory.created_at.desc())
        result = await self.db.execute(stmt)
        memories = result.scalars().all()
        return [MemoryDto.model_validate(m) for m in memories]

    async def create_memory(self, user_id: str, request: MemoryCreateRequest) -> MemoryDto:
        if not request.content.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Memory content cannot be empty.")

        memory = Memory(
            user_id=user_id,
            content=request.content.strip(),
            category=request.category,
            source=request.source,
            sensitivity_level=request.sensitivity_level,
            is_enabled=request.is_enabled
        )
        self.db.add(memory)
        await self.db.commit()
        await self.db.refresh(memory)
        return MemoryDto.model_validate(memory)

    async def update_memory(self, user_id: str, memory_id: str, request: MemoryUpdateRequest) -> MemoryDto:
        stmt = select(Memory).where(Memory.id == memory_id, Memory.user_id == user_id, Memory.deleted_at == None)
        result = await self.db.execute(stmt)
        memory = result.scalar_one_or_none()
        if not memory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found.")

        if request.content is not None:
            memory.content = request.content.strip()
        if request.category is not None:
            memory.category = request.category
        if request.sensitivity_level is not None:
            memory.sensitivity_level = request.sensitivity_level
        if request.is_enabled is not None:
            memory.is_enabled = request.is_enabled

        memory.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(memory)
        return MemoryDto.model_validate(memory)

    async def delete_memory(self, user_id: str, memory_id: str) -> None:
        stmt = select(Memory).where(Memory.id == memory_id, Memory.user_id == user_id, Memory.deleted_at == None)
        result = await self.db.execute(stmt)
        memory = result.scalar_one_or_none()
        if not memory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found.")

        memory.deleted_at = datetime.now(timezone.utc)
        await self.db.commit()

    async def clear_all_memories(self, user_id: str) -> int:
        stmt = update(Memory).where(Memory.user_id == user_id, Memory.deleted_at == None).values(deleted_at=datetime.now(timezone.utc))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount

    async def get_active_memory_context(self, user_id: str) -> str:
        stmt = select(Memory).where(Memory.user_id == user_id, Memory.is_enabled == True, Memory.deleted_at == None)
        result = await self.db.execute(stmt)
        active_memories = result.scalars().all()
        if not active_memories:
            return ""

        context_lines = ["[System Context - User Approved Durable Memories]:"]
        for m in active_memories:
            context_lines.append(f"- [{m.category}]: {m.content}")
        return "\n".join(context_lines)
