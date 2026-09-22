import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.other import Reminder
from app.schemas.task import ReminderCreateRequest, ReminderDto

class ReminderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_reminders(self, user_id: str) -> List[ReminderDto]:
        stmt = select(Reminder).where(Reminder.user_id == user_id, Reminder.deleted_at == None).order_by(Reminder.scheduled_at.asc())
        result = await self.db.execute(stmt)
        reminders = result.scalars().all()
        return [ReminderDto.model_validate(r) for r in reminders]

    async def create_reminder(self, user_id: str, request: ReminderCreateRequest) -> ReminderDto:
        if not request.title.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reminder title cannot be empty.")

        reminder = Reminder(
            user_id=user_id,
            title=request.title.strip(),
            scheduled_at=request.scheduled_at,
            timezone=request.timezone,
            idempotency_key=str(uuid.uuid4())
        )
        self.db.add(reminder)
        await self.db.commit()
        await self.db.refresh(reminder)
        return ReminderDto.model_validate(reminder)

    async def delete_reminder(self, user_id: str, reminder_id: str) -> None:
        stmt = select(Reminder).where(Reminder.id == reminder_id, Reminder.user_id == user_id, Reminder.deleted_at == None)
        result = await self.db.execute(stmt)
        reminder = result.scalar_one_or_none()
        if not reminder:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found.")

        reminder.deleted_at = datetime.now(timezone.utc)
        await self.db.commit()
