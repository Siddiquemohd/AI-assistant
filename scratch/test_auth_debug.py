import asyncio
from app.core.database import engine, Base, AsyncSessionLocal
import app.models  # Imports all models so Base.metadata knows about users, refresh_tokens, etc.
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest
from fastapi import HTTPException

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        auth_service = AuthService(db)
        email = "smohdismail22@gmail.com"
        password = "password@124"

        print(f"1. Testing registration for '{email}'...")
        try:
            reg_res = await auth_service.register(RegisterRequest(
                email=email,
                password=password,
                display_name="Ismail"
            ))
            print("   -> Registration SUCCESS! User ID:", reg_res.user.id)
        except HTTPException as e:
            print(f"   -> Registration note ({e.status_code}): {e.detail}")

        print(f"\n2. Testing login for '{email}' with password '{password}'...")
        try:
            login_res = await auth_service.login(LoginRequest(
                email=email,
                password=password
            ))
            print("   -> Login SUCCESS! User ID:", login_res.user.id)
            print("   -> Access Token Generated:", login_res.access_token[:20] + "...")
        except HTTPException as e:
            print(f"   -> Login FAILED ({e.status_code}): {e.detail}")

if __name__ == "__main__":
    asyncio.run(main())
