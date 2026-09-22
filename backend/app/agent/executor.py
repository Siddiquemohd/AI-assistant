import time
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.agent.registry import TOOL_REGISTRY, ToolDefinition
from app.schemas.task import TaskCreateRequest, ReminderCreateRequest
from app.services.task_service import TaskService
from app.services.reminder_service import ReminderService

PAYMENT_APP_KEYWORDS = {
    "paytm", "gpay", "google pay", "phonepe", "paypal", "venmo",
    "stripe", "wallet", "bank", "banking", "credit", "upi",
    "cashapp", "cash app", "yuno", "revolut", "binance", "coinbase"
}

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

        elif tool_name == "web_search":
            query = params.get("query", "").strip()
            elapsed_ms = int((time.time() - start_time) * 1000)
            return {
                "status": "Success",
                "action": "open_web_search",
                "query": query,
                "summary": f"Search requested for: '{query}'",
                "execution_time_ms": elapsed_ms
            }

        elif tool_name == "make_phone_call":
            phone_number = params.get("phone_number", "").strip()
            contact_name = params.get("contact_name", "Contact").strip()
            elapsed_ms = int((time.time() - start_time) * 1000)
            return {
                "status": "Success",
                "action": "make_phone_call",
                "phone_number": phone_number,
                "contact_name": contact_name,
                "execution_time_ms": elapsed_ms
            }

        elif tool_name == "launch_app":
            app_name = str(params.get("app_name", "")).lower().strip()
            package_name = str(params.get("package_name", "")).lower().strip()

            # Safety Check: Strictly exclude financial/payment applications
            for keyword in PAYMENT_APP_KEYWORDS:
                if keyword in app_name or keyword in package_name:
                    raise PermissionError(
                        f"Security Policy Violation: Automated launch of financial/payment app '{app_name or package_name}' is strictly prohibited."
                    )

            elapsed_ms = int((time.time() - start_time) * 1000)
            return {
                "status": "Success",
                "action": "launch_app",
                "app_name": app_name,
                "package_name": package_name,
                "execution_time_ms": elapsed_ms
            }

        else:
            raise NotImplementedError(f"Execution handler for tool '{tool_name}' is not implemented.")
