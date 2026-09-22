from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = ""
    priority: str = "Medium"
    due_at: datetime | None = None

class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_at: datetime | None = None

class TaskDto(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    status: str
    priority: str
    due_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReminderCreateRequest(BaseModel):
    title: str
    scheduled_at: datetime
    timezone: str = "UTC"

class ReminderDto(BaseModel):
    id: str
    user_id: str
    title: str
    scheduled_at: datetime
    timezone: str
    idempotency_key: str
    is_enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
