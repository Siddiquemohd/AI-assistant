import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "ISAI Python FastAPI Backend" in response.json()["message"]

@pytest.mark.asyncio
async def test_register_and_login_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register
        reg_payload = {
            "email": "pyuser@example.com",
            "password": "Password123!",
            "display_name": "Python User"
        }
        res_reg = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 200
        data_reg = res_reg.json()
        assert "access_token" in data_reg
        assert data_reg["user"]["email"] == "pyuser@example.com"

        # 2. Login
        login_payload = {
            "email": "pyuser@example.com",
            "password": "Password123!"
        }
        res_login = await ac.post("/api/v1/auth/login", json=login_payload)
        assert res_login.status_code == 200
        data_login = res_login.json()
        token = data_login["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Create conversation
        res_conv = await ac.post("/api/v1/conversations", json={"title": "Python Chat"}, headers=headers)
        assert res_conv.status_code == 200
        conv_id = res_conv.json()["id"]

        # 4. Send message
        res_msg = await ac.post(f"/api/v1/conversations/{conv_id}/messages", json={"content": "Hello FastAPI"}, headers=headers)
        assert res_msg.status_code == 200
        data_msg = res_msg.json()
        assert data_msg["role"] == "assistant"
        assert "Hello FastAPI" in data_msg["content"]
