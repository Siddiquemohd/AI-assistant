from fastapi import APIRouter
from app.api.v1.endpoints import auth, conversations, memories, settings, tasks, reminders, agent

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(conversations.router)
api_router.include_router(memories.router)
api_router.include_router(settings.router)
api_router.include_router(tasks.router)
api_router.include_router(reminders.router)
api_router.include_router(agent.router)
