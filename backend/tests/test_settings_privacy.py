import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_settings_preferences_export_and_deletion_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register & Login User
        reg_payload = {
            "email": "settingsuser@example.com",
            "password": "Password123!",
            "display_name": "Settings Test User"
        }
        res_reg = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 200
        token = res_reg.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Get Default Preferences
        res_pref = await ac.get("/api/v1/settings/preferences", headers=headers)
        assert res_pref.status_code == 200
        pref_data = res_pref.json()
        assert pref_data["theme"] == "System"
        assert pref_data["voice_enabled"] is True

        # 3. Update Preferences
        patch_payload = {
            "theme": "Dark",
            "voice_enabled": False,
            "quiet_hours_start": "22:00",
            "quiet_hours_end": "07:00",
            "assistant_personality": "Friendly & Concise"
        }
        res_update = await ac.patch("/api/v1/settings/preferences", json=patch_payload, headers=headers)
        assert res_update.status_code == 200
        updated_data = res_update.json()
        assert updated_data["theme"] == "Dark"
        assert updated_data["voice_enabled"] is False
        assert updated_data["quiet_hours_start"] == "22:00"
        assert updated_data["assistant_personality"] == "Friendly & Concise"

        # 4. Export User Data
        res_export = await ac.post("/api/v1/settings/export", headers=headers)
        assert res_export.status_code == 200
        export_data = res_export.json()
        assert "user_info" in export_data
        assert export_data["user_info"]["email"] == "settingsuser@example.com"
        assert export_data["user_preferences"]["theme"] == "Dark"

        # 5. Request Account Deletion
        res_del = await ac.delete("/api/v1/settings/account", headers=headers)
        assert res_del.status_code == 200
        del_data = res_del.json()
        assert del_data["status"] == "PendingDeletion"
        assert del_data["grace_period_days"] == 14
