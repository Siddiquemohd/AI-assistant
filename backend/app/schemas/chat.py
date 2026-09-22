from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CreateConversationRequest(BaseModel):
    title: str | None = "New Conversation"

class SendMessageRequest(BaseModel):
    content: str

class ConversationDto(BaseModel):
    id: str
    title: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageDto(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    message_type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
