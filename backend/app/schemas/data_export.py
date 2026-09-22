from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel

class UserDataExportDto(BaseModel):
    user_id: str
    exported_at: datetime
    user_info: Dict[str, Any]
    user_preferences: Dict[str, Any]
    conversations: List[Dict[str, Any]]
    memories: List[Dict[str, Any]]
    tasks: List[Dict[str, Any]]
    reminders: List[Dict[str, Any]]
