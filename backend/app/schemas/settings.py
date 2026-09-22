from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserPreferenceDto(BaseModel):
    user_id: str
    theme: str
    timezone: str
    voice_enabled: bool
    proactive_assistance: bool
    quiet_hours_start: str
    quiet_hours_end: str
    assistant_personality: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserPreferenceUpdateRequest(BaseModel):
    theme: str | None = None
    timezone: str | None = None
    voice_enabled: bool | None = None
    proactive_assistance: bool | None = None
    quiet_hours_start: str | None = None
    quiet_hours_end: str | None = None
    assistant_personality: str | None = None
