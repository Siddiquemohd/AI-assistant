from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict

class AgentRunRequest(BaseModel):
    intent: str
    conversation_id: str | None = None

class ToolExecutionDto(BaseModel):
    id: str
    agent_run_id: str
    tool_name: str
    tool_version: str
    input_metadata: Dict[str, Any]
    status: str
    result_metadata: Dict[str, Any]
    execution_time_ms: int
    started_at: datetime
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class AgentRunDto(BaseModel):
    id: str
    user_id: str
    conversation_id: str | None = None
    intent: str
    status: str
    risk_level: str
    requires_confirmation: bool
    confirmation_token_digest: str
    started_at: datetime
    completed_at: datetime | None = None
    tool_executions: List[ToolExecutionDto] = []

    model_config = ConfigDict(from_attributes=True)

class AgentConfirmRequest(BaseModel):
    confirmation_token_digest: str
