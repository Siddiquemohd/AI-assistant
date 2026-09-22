from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, RefreshToken, UserPreference
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshTokenRequest, AuthResponse, UserDto
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, request: RegisterRequest) -> AuthResponse:
        email = request.email.strip().lower()
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists.")

        display_name = request.display_name.strip() if request.display_name else email.split("@")[0]
        user = User(
            email=email,
            password_hash=hash_password(request.password),
            display_name=display_name
        )
        self.db.add(user)
        await self.db.flush()

        user_pref = UserPreference(user_id=user.id)
        self.db.add(user_pref)

        access_token, access_exp = create_access_token(user.id, user.email, user.display_name)
        refresh_token, refresh_exp = create_refresh_token()

        rt_entity = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=refresh_exp
        )
        self.db.add(rt_entity)
        await self.db.commit()

        return AuthResponse(
            access_token=access_token,
            access_token_expires_at=access_exp,
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_exp,
            user=UserDto(id=user.id, email=user.email, display_name=user.display_name)
        )

    async def login(self, request: LoginRequest) -> AuthResponse:
        email = request.email.strip().lower()
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(request.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

        access_token, access_exp = create_access_token(user.id, user.email, user.display_name)
        refresh_token, refresh_exp = create_refresh_token()

        rt_entity = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=refresh_exp
        )
        self.db.add(rt_entity)
        await self.db.commit()

        return AuthResponse(
            access_token=access_token,
            access_token_expires_at=access_exp,
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_exp,
            user=UserDto(id=user.id, email=user.email, display_name=user.display_name)
        )

    async def refresh_token(self, request: RefreshTokenRequest) -> AuthResponse:
        stmt = select(RefreshToken).where(RefreshToken.token == request.refresh_token, RefreshToken.is_revoked == False)
        result = await self.db.execute(stmt)
        rt_entity = result.scalar_one_or_none()

        if not rt_entity or rt_entity.expires_at <= datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token.")

        rt_entity.is_revoked = True

        stmt_user = select(User).where(User.id == rt_entity.user_id)
        res_user = await self.db.execute(stmt_user)
        user = res_user.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

        new_access, new_access_exp = create_access_token(user.id, user.email, user.display_name)
        new_refresh, new_refresh_exp = create_refresh_token()

        new_rt = RefreshToken(
            user_id=user.id,
            token=new_refresh,
            expires_at=new_refresh_exp
        )
        self.db.add(new_rt)
        await self.db.commit()

        return AuthResponse(
            access_token=new_access,
            access_token_expires_at=new_access_exp,
            refresh_token=new_refresh,
            refresh_token_expires_at=new_refresh_exp,
            user=UserDto(id=user.id, email=user.email, display_name=user.display_name)
        )
