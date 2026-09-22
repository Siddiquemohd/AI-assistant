import time
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.agent.registry import TOOL_REGISTRY, ToolDefinition
from app.schemas.task import TaskCreateRequest, ReminderCreateRequest
from app.services.task_service import TaskService
from app.services.reminder_service import ReminderService

class ToolExecutor:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_service = TaskService(db)
        self.reminder_service = ReminderService(db)

    async def execute_tool(self, user_id: str, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in TOOL_REGISTRY:
            raise ValueError(f"Tool '{tool_name}' is not in allowlisted tool registry.")

        tool_def = TOOL_REGISTRY[tool_name]
        start_time = time.time()

        if tool_name == "create_task":
            req = TaskCreateRequest(
                title=params.get("title", "New Task"),
                description=params.get("description", ""),
                priority=params.get("priority", "Medium"),
                due_at=params.get("due_at")
            )
            result_dto = await self.task_service.create_task(user_id, req)
            elapsed_ms = int((time.time() - start_time) * 1000)
            return {"status": "Success", "task": result_dto.model_dump(mode='json'), "execution_time_ms": elapsed_ms}

        elif tool_name == "create_reminder":
            req = ReminderCreateRequest(
                title=params.get("title", "New Reminder"),
                scheduled_at=params.get("scheduled_at"),
                timezone=params.get("timezone", "UTC")
            )
            result_dto = await self.reminder_service.create_reminder(user_id, req)
            elapsed_ms = int((time.time() - start_time) * 1000)
            return {"status": "Success", "reminder": result_dto.model_dump(mode='json'), "execution_time_ms": elapsed_ms}

        elif tool_name == "delete_task":
            task_id = params.get("task_id")
            await self.task_service.delete_task(user_id, task_id)
            elapsed_ms = int((time.time() - start_time) * 1000)
            return {"status": "Success", "deleted_task_id": task_id, "execution_time_ms": elapsed_ms}

        elif tool_name == "search_history":
            elapsed_ms = int((time.time() - start_time) * 1000)
            return {"status": "Success", "matches": [], "execution_time_ms": elapsed_ms}

        else:
            raise NotImplementedError(f"Execution handler for tool '{tool_name}' is not implemented.")
