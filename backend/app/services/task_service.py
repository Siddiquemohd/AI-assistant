from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.other import TaskItem
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskDto

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(self, user_id: str) -> List[TaskDto]:
        stmt = select(TaskItem).where(TaskItem.user_id == user_id, TaskItem.deleted_at == None).order_by(TaskItem.created_at.desc())
        result = await self.db.execute(stmt)
        tasks = result.scalars().all()
        return [TaskDto.model_validate(t) for t in tasks]

    async def create_task(self, user_id: str, request: TaskCreateRequest) -> TaskDto:
        if not request.title.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task title cannot be empty.")

        task = TaskItem(
            user_id=user_id,
            title=request.title.strip(),
            description=request.description or "",
            priority=request.priority,
            due_at=request.due_at,
            status="Pending"
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return TaskDto.model_validate(task)

    async def update_task(self, user_id: str, task_id: str, request: TaskUpdateRequest) -> TaskDto:
        stmt = select(TaskItem).where(TaskItem.id == task_id, TaskItem.user_id == user_id, TaskItem.deleted_at == None)
        result = await self.db.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

        if request.title is not None:
            task.title = request.title.strip()
        if request.description is not None:
            task.description = request.description
        if request.priority is not None:
            task.priority = request.priority
        if request.status is not None:
            task.status = request.status
            if request.status == "Completed" and not task.completed_at:
                task.completed_at = datetime.now(timezone.utc)
        if request.due_at is not None:
            task.due_at = request.due_at

        await self.db.commit()
        await self.db.refresh(task)
        return TaskDto.model_validate(task)

    async def delete_task(self, user_id: str, task_id: str) -> None:
        stmt = select(TaskItem).where(TaskItem.id == task_id, TaskItem.user_id == user_id, TaskItem.deleted_at == None)
        result = await self.db.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

        task.deleted_at = datetime.now(timezone.utc)
        await self.db.commit()
