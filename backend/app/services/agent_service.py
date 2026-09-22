import json
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.agent import AgentRun, ToolExecution
from app.schemas.agent import AgentRunRequest, AgentRunDto, AgentConfirmRequest
from app.agent.registry import TOOL_REGISTRY
from app.agent.executor import ToolExecutor
from app.agent.safety import generate_confirmation_token_digest, validate_confirmation_token_digest

class AgentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_agent_run(self, user_id: str, run_id: str) -> AgentRunDto:
        stmt = select(AgentRun).options(selectinload(AgentRun.tool_executions)).where(AgentRun.id == run_id, AgentRun.user_id == user_id)
        res = await self.db.execute(stmt)
        run = res.scalar_one_or_none()
        if not run:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent run not found.")
        return AgentRunDto.model_validate(run)

    async def create_agent_run(self, user_id: str, request: AgentRunRequest) -> AgentRunDto:
        intent = request.intent.strip().lower()
        tool_name = "create_task"
        params = {"title": request.intent.strip()}

        if "delete" in intent:
            tool_name = "delete_task"
            words = request.intent.strip().split()
            target_id = words[-1] if len(words) > 1 else ""
            params = {"task_id": target_id}
        elif "remind" in intent:
            tool_name = "create_reminder"
            params = {"title": request.intent.strip(), "scheduled_at": datetime.now(timezone.utc).isoformat()}

        tool_def = TOOL_REGISTRY[tool_name]
        requires_conf = tool_def.requires_confirmation

        run = AgentRun(
            user_id=user_id,
            conversation_id=request.conversation_id,
            intent=request.intent,
            status="AwaitingConfirmation" if requires_conf else "Authorized",
            risk_level=tool_def.risk_level,
            requires_confirmation=requires_conf
        )
        self.db.add(run)
        await self.db.flush()

        digest = generate_confirmation_token_digest(run.id, tool_name, params)
        run.confirmation_token_digest = digest

        if not requires_conf:
            executor = ToolExecutor(self.db)
            tool_exec = ToolExecution(
                agent_run_id=run.id,
                tool_name=tool_name,
                tool_version=tool_def.version,
                input_metadata=params,
                status="Executing"
            )
            self.db.add(tool_exec)
            await self.db.flush()

            res = await executor.execute_tool(user_id, tool_name, params)
            tool_exec.status = "Completed"
            tool_exec.result_metadata = res
            tool_exec.execution_time_ms = res.get("execution_time_ms", 0)
            tool_exec.completed_at = datetime.now(timezone.utc)

            run.status = "Completed"
            run.completed_at = datetime.now(timezone.utc)

        await self.db.commit()
        return await self.get_agent_run(user_id, run.id)

    async def confirm_agent_run(self, user_id: str, run_id: str, request: AgentConfirmRequest) -> AgentRunDto:
        stmt = select(AgentRun).options(selectinload(AgentRun.tool_executions)).where(AgentRun.id == run_id, AgentRun.user_id == user_id)
        res = await self.db.execute(stmt)
        run = res.scalar_one_or_none()
        if not run:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent run not found.")

        if run.status != "AwaitingConfirmation":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agent run is not awaiting confirmation.")

        tool_name = "delete_task"
        words = run.intent.strip().split()
        target_id = words[-1] if len(words) > 1 else ""
        params = {"task_id": target_id}

        if not validate_confirmation_token_digest(run.id, tool_name, params, request.confirmation_token_digest):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or stale confirmation token digest.")

        run.status = "Authorized"
        executor = ToolExecutor(self.db)
        tool_exec = ToolExecution(
            agent_run_id=run.id,
            tool_name=tool_name,
            input_metadata=params,
            status="Executing"
        )
        self.db.add(tool_exec)
        await self.db.flush()

        res = await executor.execute_tool(user_id, tool_name, params)
        tool_exec.status = "Completed"
        tool_exec.result_metadata = res
        tool_exec.execution_time_ms = res.get("execution_time_ms", 0)
        tool_exec.completed_at = datetime.now(timezone.utc)

        run.status = "Completed"
        run.completed_at = datetime.now(timezone.utc)

        await self.db.commit()
        return await self.get_agent_run(user_id, run.id)
