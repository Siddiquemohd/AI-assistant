from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user_id
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskDto
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=List[TaskDto])
async def get_tasks(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    return await service.get_tasks(user_id)

@router.post("", response_model=TaskDto, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    return await service.create_task(user_id, request)

@router.patch("/{task_id}", response_model=TaskDto)
async def update_task(
    task_id: str,
    request: TaskUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    return await service.update_task(user_id, task_id, request)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = TaskService(db)
    await service.delete_task(user_id, task_id)
