from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.user import User, UserPreference
from app.models.conversation import Conversation, Message
from app.models.other import Memory, TaskItem, Reminder
from app.schemas.settings import UserPreferenceDto, UserPreferenceUpdateRequest
from app.schemas.data_export import UserDataExportDto

class SettingsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_preferences(self, user_id: str) -> UserPreferenceDto:
        stmt = select(UserPreference).where(UserPreference.user_id == user_id)
        result = await self.db.execute(stmt)
        pref = result.scalar_one_or_none()
        if not pref:
            pref = UserPreference(user_id=user_id)
            self.db.add(pref)
            await self.db.commit()
            await self.db.refresh(pref)
        return UserPreferenceDto.model_validate(pref)

    async def update_user_preferences(self, user_id: str, request: UserPreferenceUpdateRequest) -> UserPreferenceDto:
        stmt = select(UserPreference).where(UserPreference.user_id == user_id)
        result = await self.db.execute(stmt)
        pref = result.scalar_one_or_none()
        if not pref:
            pref = UserPreference(user_id=user_id)
            self.db.add(pref)

        if request.theme is not None:
            pref.theme = request.theme
        if request.timezone is not None:
            pref.timezone = request.timezone
        if request.voice_enabled is not None:
            pref.voice_enabled = request.voice_enabled
        if request.proactive_assistance is not None:
            pref.proactive_assistance = request.proactive_assistance
        if request.quiet_hours_start is not None:
            pref.quiet_hours_start = request.quiet_hours_start
        if request.quiet_hours_end is not None:
            pref.quiet_hours_end = request.quiet_hours_end
        if request.assistant_personality is not None:
            pref.assistant_personality = request.assistant_personality

        pref.updated_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(pref)
        return UserPreferenceDto.model_validate(pref)

    async def export_user_data(self, user_id: str) -> UserDataExportDto:
        res_user = await self.db.execute(select(User).where(User.id == user_id))
        user = res_user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        pref = await self.get_user_preferences(user_id)

        res_convs = await self.db.execute(select(Conversation).where(Conversation.user_id == user_id, Conversation.deleted_at == None))
        convs = res_convs.scalars().all()

        res_mems = await self.db.execute(select(Memory).where(Memory.user_id == user_id, Memory.deleted_at == None))
        mems = res_mems.scalars().all()

        res_tasks = await self.db.execute(select(TaskItem).where(TaskItem.user_id == user_id, TaskItem.deleted_at == None))
        tasks = res_tasks.scalars().all()

        res_rems = await self.db.execute(select(Reminder).where(Reminder.user_id == user_id, Reminder.deleted_at == None))
        rems = res_rems.scalars().all()

        return UserDataExportDto(
            user_id=user_id,
            exported_at=datetime.now(timezone.utc),
            user_info={"email": user.email, "display_name": user.display_name, "created_at": user.created_at.isoformat()},
            user_preferences=pref.model_dump(mode='json'),
            conversations=[{"id": c.id, "title": c.title, "created_at": c.created_at.isoformat()} for c in convs],
            memories=[{"id": m.id, "content": m.content, "category": m.category} for m in mems],
            tasks=[{"id": t.id, "title": t.title, "status": t.status} for t in tasks],
            reminders=[{"id": r.id, "title": r.title, "scheduled_at": r.scheduled_at.isoformat()} for r in rems]
        )

    async def request_account_deletion(self, user_id: str) -> dict:
        now = datetime.now(timezone.utc)
        await self.db.execute(update(Conversation).where(Conversation.user_id == user_id).values(deleted_at=now))
        await self.db.execute(update(Memory).where(Memory.user_id == user_id).values(deleted_at=now))
        await self.db.execute(update(TaskItem).where(TaskItem.user_id == user_id).values(deleted_at=now))
        await self.db.execute(update(Reminder).where(Reminder.user_id == user_id).values(deleted_at=now))
        await self.db.commit()
        return {"status": "PendingDeletion", "user_id": user_id, "grace_period_days": 14, "requested_at": now.isoformat()}
