import json
from datetime import datetime, timezone
from typing import AsyncGenerator, List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.conversation import Conversation, Message
from app.schemas.chat import ConversationDto, MessageDto, CreateConversationRequest, SendMessageRequest
from app.services.memory_service import MemoryService
from app.ai.gateway import AiGateway
from app.ai.base import PromptMessage

class ChatService:
    def __init__(self, db: AsyncSession, ai_gateway: AiGateway):
        self.db = db
        self.ai_gateway = ai_gateway

    async def get_conversations(self, user_id: str) -> List[ConversationDto]:
        stmt = select(Conversation).where(Conversation.user_id == user_id, Conversation.deleted_at == None).order_by(Conversation.updated_at.desc())
        result = await self.db.execute(stmt)
        convs = result.scalars().all()
        return [ConversationDto.model_validate(c) for c in convs]

    async def create_conversation(self, user_id: str, request: CreateConversationRequest) -> ConversationDto:
        title = request.title.strip() if request.title else "New Conversation"
        conv = Conversation(user_id=user_id, title=title, status="Active")
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return ConversationDto.model_validate(conv)

    async def get_messages(self, user_id: str, conversation_id: str, page: int = 1, page_size: int = 50) -> List[MessageDto]:
        stmt_conv = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id, Conversation.deleted_at == None)
        res_conv = await self.db.execute(stmt_conv)
        if not res_conv.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")

        skip = (page - 1) * page_size
        stmt_msg = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).offset(skip).limit(page_size)
        res_msg = await self.db.execute(stmt_msg)
        msgs = res_msg.scalars().all()
        return [MessageDto.model_validate(m) for m in msgs]

    async def send_message(self, user_id: str, conversation_id: str, request: SendMessageRequest) -> MessageDto:
        stmt_conv = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id, Conversation.deleted_at == None)
        res_conv = await self.db.execute(stmt_conv)
        conv = res_conv.scalar_one_or_none()
        if not conv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")

        user_msg = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=request.content.strip(),
            message_type="Text",
            status="Completed"
        )
        self.db.add(user_msg)

        if conv.title == "New Conversation":
            conv.title = request.content.strip()[:30] + ("..." if len(request.content.strip()) > 30 else "")
        conv.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

        # Build prompt history with User-Approved Memory injection
        stmt_history = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        res_history = await self.db.execute(stmt_history)
        history_msgs = res_history.scalars().all()

        memory_service = MemoryService(self.db)
        memory_context = await memory_service.get_active_memory_context(user_id)

        prompt_history: List[PromptMessage] = []
        if memory_context:
            prompt_history.append(PromptMessage(role="system", content=memory_context))

        prompt_history.extend([PromptMessage(role=m.role, content=m.content) for m in history_msgs])

        ai_response_text = await self.ai_gateway.generate_response(prompt_history)

        assistant_msg = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=ai_response_text,
            message_type="Text",
            status="Completed",
            model_name="ISAI-FastAPI-Gateway"
        )
        self.db.add(assistant_msg)
        await self.db.commit()
        await self.db.refresh(assistant_msg)

        return MessageDto.model_validate(assistant_msg)

    async def stream_message(self, user_id: str, conversation_id: str, request: SendMessageRequest) -> AsyncGenerator[dict, None]:
        stmt_conv = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id, Conversation.deleted_at == None)
        res_conv = await self.db.execute(stmt_conv)
        conv = res_conv.scalar_one_or_none()
        if not conv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")

        user_msg = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=request.content.strip(),
            message_type="Text",
            status="Completed"
        )
        self.db.add(user_msg)

        if conv.title == "New Conversation":
            conv.title = request.content.strip()[:30] + ("..." if len(request.content.strip()) > 30 else "")
        conv.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

        assistant_msg = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content="",
            message_type="Text",
            status="Processing",
            model_name="ISAI-FastAPI-Gateway"
        )
        self.db.add(assistant_msg)
        await self.db.commit()
        await self.db.refresh(assistant_msg)

        yield {
            "event": "message.started",
            "data": json.dumps({
                "messageId": assistant_msg.id,
                "conversationId": conversation_id,
                "role": "assistant",
                "createdAt": assistant_msg.created_at.isoformat()
            })
        }

        # Build prompt history with User-Approved Memory injection
        stmt_history = select(Message).where(Message.conversation_id == conversation_id, Message.id != assistant_msg.id).order_by(Message.created_at.asc())
        res_history = await self.db.execute(stmt_history)
        history_msgs = res_history.scalars().all()

        memory_service = MemoryService(self.db)
        memory_context = await memory_service.get_active_memory_context(user_id)

        prompt_history: List[PromptMessage] = []
        if memory_context:
            prompt_history.append(PromptMessage(role="system", content=memory_context))

        prompt_history.extend([PromptMessage(role=m.role, content=m.content) for m in history_msgs])

        full_content = []
        delta_index = 0

        async for chunk in self.ai_gateway.stream_response(prompt_history):
            full_content.append(chunk)
            yield {
                "event": "message.delta",
                "data": json.dumps({
                    "messageId": assistant_msg.id,
                    "chunk": chunk,
                    "deltaIndex": delta_index
                })
            }
            delta_index += 1

        assistant_msg.content = "".join(full_content)
        assistant_msg.status = "Completed"
        await self.db.commit()

        yield {
            "event": "message.completed",
            "data": json.dumps({
                "messageId": assistant_msg.id,
                "fullContent": assistant_msg.content,
                "status": "Completed",
                "persistedAt": datetime.now(timezone.utc).isoformat()
            })
        }
