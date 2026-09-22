from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user_id
from app.schemas.settings import UserPreferenceDto, UserPreferenceUpdateRequest
from app.schemas.data_export import UserDataExportDto
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/preferences", response_model=UserPreferenceDto)
async def get_preferences(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = SettingsService(db)
    return await service.get_user_preferences(user_id)

@router.patch("/preferences", response_model=UserPreferenceDto)
async def update_preferences(
    request: UserPreferenceUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = SettingsService(db)
    return await service.update_user_preferences(user_id, request)

@router.post("/export", response_model=UserDataExportDto)
async def export_user_data(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = SettingsService(db)
    return await service.export_user_data(user_id)

@router.delete("/account")
async def delete_account(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = SettingsService(db)
    return await service.request_account_deletion(user_id)

