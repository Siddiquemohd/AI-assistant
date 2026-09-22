import asyncio
import re
from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage

class MockAiProvider(BaseAiProvider):
    @property
    def name(self) -> str:
        return "ISAI-AutonomousEngine"

    def _parse_intent(self, user_text: str) -> str:
        text_lower = user_text.lower().strip()

        # Phone Call Intent
        if any(w in text_lower for w in ["call ", "dial ", "phone "]):
            match = re.search(r'(?:call|dial|phone)\s+([a-zA-Z0-9\s\+\-]+)', text_lower)
            target = match.group(1).strip() if match else "contact"
            return f"📱 **Autonomous Phone Intent**: Initiating call to '{target}'. Proceeding with device call intent."

        # Web Search Intent
        if any(w in text_lower for w in ["search ", "google ", "find online ", "look up "]):
            match = re.search(r'(?:search|google|find online|look up)\s+(?:for\s+)?(.+)', text_lower)
            query = match.group(1).strip() if match else text_lower
            return f"🌐 **Autonomous Web Search**: Searching for '{query}'. Opening search results."

        # App Launch Intent
        if any(w in text_lower for w in ["open ", "launch ", "start app "]):
            match = re.search(r'(?:open|launch|start app)\s+([a-zA-Z0-9\s]+)', text_lower)
            app = match.group(1).strip() if match else "app"

            # Check financial safety blacklist
            financial_terms = ["gpay", "paytm", "phonepe", "bank", "wallet", "paypal", "stripe", "upi"]
            if any(term in app for term in financial_terms):
                return f"⚠️ **Security Exclusion**: Autonomous launch of payment/financial app '{app}' is strictly prohibited for security."

            return f"🚀 **Autonomous App Launcher**: Opening application '{app}'."

        # Task Creation Intent
        if any(w in text_lower for w in ["create task", "add task", "todo"]):
            return f"✅ **Autonomous Task Agent**: Creating task based on your directive: '{user_text}'."

        # Reminder Intent
        if any(w in text_lower for w in ["remind me", "set reminder"]):
            return f"⏰ **Autonomous Reminder Agent**: Scheduling reminder: '{user_text}'."

        # Memory Intent
        if any(w in text_lower for w in ["remember ", "keep in mind"]):
            return f"🧠 **Autonomous Memory Bank**: Saved directive to durable memory: '{user_text}'."

        # General Autonomous Conversation Response
        return f"I am ISAI, operating 100% autonomously on your system. I processed your prompt: '{user_text}'. All device automation tools (Calls, Web Search, App Launcher, Tasks, Memories) are active."

    async def generate_response(self, history: List[PromptMessage]) -> str:
        last_user_msg = next((m.content for m in reversed(history) if m.role == "user"), "Hello")
        return self._parse_intent(last_user_msg)

    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        full_response = await self.generate_response(history)
        words = full_response.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.03)
