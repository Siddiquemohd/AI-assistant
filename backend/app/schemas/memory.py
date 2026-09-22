from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MemoryCreateRequest(BaseModel):
    content: str
    category: str = "General"
    source: str = "UserExplicit"
    sensitivity_level: str = "Normal"
    is_enabled: bool = True

class MemoryUpdateRequest(BaseModel):
    content: str | None = None
    category: str | None = None
    sensitivity_level: str | None = None
    is_enabled: bool | None = None

class MemoryDto(BaseModel):
    id: str
    user_id: str
    content: str
    category: str
    source: str
    sensitivity_level: str
    is_enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
