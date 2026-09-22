from typing import List
from fastapi import APIRouter, Depends, Query
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user_id
from app.schemas.chat import ConversationDto, MessageDto, CreateConversationRequest, SendMessageRequest
from app.services.chat_service import ChatService
from app.ai.gateway import AiGateway

router = APIRouter(prefix="/conversations", tags=["Conversations"])
ai_gateway = AiGateway()

@router.get("", response_model=List[ConversationDto])
async def get_conversations(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    chat_service = ChatService(db, ai_gateway)
    return await chat_service.get_conversations(user_id)

@router.post("", response_model=ConversationDto)
async def create_conversation(
    request: CreateConversationRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    chat_service = ChatService(db, ai_gateway)
    return await chat_service.create_conversation(user_id, request)

@router.get("/{conversation_id}/messages", response_model=List[MessageDto])
async def get_messages(
    conversation_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    chat_service = ChatService(db, ai_gateway)
    return await chat_service.get_messages(user_id, conversation_id, page, page_size)

@router.post("/{conversation_id}/messages", response_model=MessageDto)
async def send_message(
    conversation_id: str,
    request: SendMessageRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    chat_service = ChatService(db, ai_gateway)
    return await chat_service.send_message(user_id, conversation_id, request)

@router.post("/{conversation_id}/messages/stream")
async def stream_message(
    conversation_id: str,
    request: SendMessageRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    chat_service = ChatService(db, ai_gateway)
    event_generator = chat_service.stream_message(user_id, conversation_id, request)
    return EventSourceResponse(event_generator)
