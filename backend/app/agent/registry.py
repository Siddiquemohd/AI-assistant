from typing import Any, Dict
from pydantic import BaseModel

class ToolDefinition(BaseModel):
    name: str
    version: str = "1.0"
    description: str
    risk_level: str  # Low, Medium, High, Critical
    requires_confirmation: bool
    is_read_only: bool
    timeout_ms: int = 15000

TOOL_REGISTRY: Dict[str, ToolDefinition] = {
    "create_task": ToolDefinition(
        name="create_task",
        description="Creates a new task item for the user.",
        risk_level="Low",
        requires_confirmation=False,
        is_read_only=False,
    ),
    "create_reminder": ToolDefinition(
        name="create_reminder",
        description="Schedules a reminder for the user.",
        risk_level="Medium",
        requires_confirmation=False,
        is_read_only=False,
    ),
    "delete_task": ToolDefinition(
        name="delete_task",
        description="Deletes a user task by ID.",
        risk_level="High",
        requires_confirmation=True,
        is_read_only=False,
    ),
    "search_history": ToolDefinition(
        name="search_history",
        description="Searches user conversation history.",
        risk_level="Low",
        requires_confirmation=False,
        is_read_only=True,
    ),
}
