from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user_id
from app.schemas.memory import MemoryCreateRequest, MemoryUpdateRequest, MemoryDto
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/memories", tags=["Memories"])

@router.get("", response_model=List[MemoryDto])
async def get_memories(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = MemoryService(db)
    return await service.get_memories(user_id)

@router.post("", response_model=MemoryDto, status_code=status.HTTP_201_CREATED)
async def create_memory(
    request: MemoryCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = MemoryService(db)
    return await service.create_memory(user_id, request)

@router.patch("/{memory_id}", response_model=MemoryDto)
async def update_memory(
    memory_id: str,
    request: MemoryUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = MemoryService(db)
    return await service.update_memory(user_id, memory_id, request)

@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = MemoryService(db)
    await service.delete_memory(user_id, memory_id)

@router.post("/clear")
async def clear_all_memories(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = MemoryService(db)
    count = await service.clear_all_memories(user_id)
    return {"message": "All memories cleared successfully.", "count": count}
