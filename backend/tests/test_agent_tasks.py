import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_tasks_reminders_and_agent_confirmation_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register & Login
        reg_payload = {
            "email": "agentuser@example.com",
            "password": "Password123!",
            "display_name": "Agent User"
        }
        res_reg = await ac.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 200
        token = res_reg.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Create Task directly
        task_payload = {"title": "Buy groceries", "priority": "High"}
        res_task = await ac.post("/api/v1/tasks", json=task_payload, headers=headers)
        assert res_task.status_code == 201
        task_data = res_task.json()
        task_id = task_data["id"]
        assert task_data["title"] == "Buy groceries"

        # 3. Create Low-Risk Agent Run (create_task tool)
        agent_req = {"intent": "Create a task to finish report"}
        res_agent = await ac.post("/api/v1/agent/runs", json=agent_req, headers=headers)
        assert res_agent.status_code == 201
        run_data = res_agent.json()
        assert run_data["status"] == "Completed"
        assert len(run_data["tool_executions"]) == 1

        # 4. Create High-Risk Agent Run (delete_task tool, requires confirmation)
        del_agent_req = {"intent": f"Delete task {task_id}"}
        res_del_agent = await ac.post("/api/v1/agent/runs", json=del_agent_req, headers=headers)
        assert res_del_agent.status_code == 201
        del_run_data = res_del_agent.json()
        assert del_run_data["status"] == "AwaitingConfirmation"
        assert del_run_data["requires_confirmation"] is True
        run_id = del_run_data["id"]
        digest = del_run_data["confirmation_token_digest"]

        # 5. Confirm High-Risk Agent Run
        confirm_req = {"confirmation_token_digest": digest}
        res_confirm = await ac.post(f"/api/v1/agent/runs/{run_id}/confirm", json=confirm_req, headers=headers)
        assert res_confirm.status_code == 200
        confirmed_data = res_confirm.json()
        assert confirmed_data["status"] == "Completed"
