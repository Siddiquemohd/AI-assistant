import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_memory_crud_and_prompt_context_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register & Login
        reg_payload = {
            "email": "memuser@example.com",
            "password": "Password123!",
            "display_name": "Memory User"
        }
        res_reg = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 200
        token = res_reg.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Create Memory
        mem_payload = {
            "content": "User prefers concise python responses",
            "category": "Preference",
            "sensitivity_level": "Normal",
            "is_enabled": True
        }
        res_mem = await ac.post("/api/v1/memories", json=mem_payload, headers=headers)
        assert res_mem.status_code == 201
        mem_data = res_mem.json()
        assert mem_data["content"] == "User prefers concise python responses"
        mem_id = mem_data["id"]

        # 3. List Memories
        res_list = await ac.get("/api/v1/memories", headers=headers)
        assert res_list.status_code == 200
        assert len(res_list.json()) == 1

        # 4. Toggle Disable Memory
        res_patch = await ac.patch(f"/api/v1/memories/{mem_id}", json={"is_enabled": False}, headers=headers)
        assert res_patch.status_code == 200
        assert res_patch.json()["is_enabled"] is False

        # 5. Toggle Re-enable Memory
        res_patch2 = await ac.patch(f"/api/v1/memories/{mem_id}", json={"is_enabled": True}, headers=headers)
        assert res_patch2.status_code == 200
        assert res_patch2.json()["is_enabled"] is True

        # 6. Delete Memory
        res_del = await ac.delete(f"/api/v1/memories/{mem_id}", headers=headers)
        assert res_del.status_code == 204

        # 7. List should be empty after soft delete
        res_list2 = await ac.get("/api/v1/memories", headers=headers)
        assert res_list2.status_code == 200
        assert len(res_list2.json()) == 0
