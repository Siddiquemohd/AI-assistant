from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user_id
from app.schemas.agent import AgentRunRequest, AgentRunDto, AgentConfirmRequest
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/runs", response_model=AgentRunDto, status_code=status.HTTP_201_CREATED)
async def create_agent_run(
    request: AgentRunRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = AgentService(db)
    return await service.create_agent_run(user_id, request)

@router.get("/runs/{run_id}", response_model=AgentRunDto)
async def get_agent_run(
    run_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = AgentService(db)
    return await service.get_agent_run(user_id, run_id)

@router.post("/runs/{run_id}/confirm", response_model=AgentRunDto)
async def confirm_agent_run(
    run_id: str,
    request: AgentConfirmRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = AgentService(db)
    return await service.confirm_agent_run(user_id, run_id, request)
