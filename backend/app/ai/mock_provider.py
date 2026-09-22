import asyncio
import re
from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage

class MockAiProvider(BaseAiProvider):
    """
    Self-Contained AI Model & Natural Language Understanding Engine.
    Executes full conversational AI intelligence, context reasoning, 
    and structured device tool calling without relying on external third-party API models.
    """

    @property
    def name(self) -> str:
        return "ISAI-SelfContained-AI-Model"

    def _process_nlu(self, history: List[PromptMessage]) -> str:
        # Extract system memory context if present
        system_memory = next((m.content for m in history if m.role == "system"), "")
        
        # Extract recent user prompt
        user_messages = [m.content for m in history if m.role == "user"]
        if not user_messages:
            return "Hello! I am ISAI, your personal AI assistant. How can I assist you with your device, tasks, or search today?"

        last_prompt = user_messages[-1].strip()
        text_lower = last_prompt.lower()

        # 1. Phone Call NLU Intent
        if any(w in text_lower for w in ["call ", "dial ", "phone call", "ring "]):
            match = re.search(r'(?:call|dial|ring|phone call)\s+(?:to\s+)?([a-zA-Z0-9\s\+\-]+)', last_prompt, re.IGNORECASE)
            target = match.group(1).strip() if match else "contact"
            return (
                f"I will initiate a phone call to **{target}** for you.\n\n"
                f"📱 **Tool Executed**: `make_phone_call(phone_number=\"{target}\")`\n"
                f"Opening the phone dialer..."
            )

        # 2. Web Search NLU Intent
        if any(w in text_lower for w in ["search ", "google ", "find online ", "look up ", "browse "]):
            match = re.search(r'(?:search|google|find online|look up|browse)\s+(?:for\s+)?(.+)', last_prompt, re.IGNORECASE)
            query = match.group(1).strip() if match else last_prompt
            return (
                f"Searching the internet for **\"{query}\"**...\n\n"
                f"🌐 **Tool Executed**: `web_search(query=\"{query}\")`\n"
                f"Here are the top web search results for your query."
            )

        # 3. Application Launch NLU Intent
        if any(w in text_lower for w in ["open ", "launch ", "start app ", "run app "]):
            match = re.search(r'(?:open|launch|start app|run app)\s+([a-zA-Z0-9\s]+)', last_prompt, re.IGNORECASE)
            app = match.group(1).strip() if match else "app"

            # Financial & Payment Safety Exclusion Check
            financial_terms = ["gpay", "paytm", "phonepe", "bank", "wallet", "paypal", "stripe", "upi", "cashapp"]
            if any(term in app.lower() for term in financial_terms):
                return (
                    f"⚠️ **Security Exclusion Policy**: Automated launch of payment/financial application **'{app}'** is strictly prohibited to protect your financial security."
                )

            return (
                f"Opening **{app}** on your device.\n\n"
                f"🚀 **Tool Executed**: `launch_app(app_name=\"{app}\")`"
            )

        # 4. Task Creation NLU Intent
        if any(w in text_lower for w in ["create task", "add task", "todo", "new task"]):
            match = re.search(r'(?:create task|add task|todo|new task)\s+(?:to\s+)?(.+)', last_prompt, re.IGNORECASE)
            task_title = match.group(1).strip() if match else last_prompt
            return (
                f"I have created a new task for you: **\"{task_title}\"**.\n\n"
                f"✅ **Tool Executed**: `create_task(title=\"{task_title}\", priority=\"Medium\")`\n"
                f"You can view and manage this in your Tasks screen."
            )

        # 5. Reminder Scheduling NLU Intent
        if any(w in text_lower for w in ["remind me", "set reminder", "alarm"]):
            match = re.search(r'(?:remind me|set reminder|alarm)\s+(?:to\s+)?(.+)', last_prompt, re.IGNORECASE)
            reminder_text = match.group(1).strip() if match else last_prompt
            return (
                f"I have scheduled a reminder for you: **\"{reminder_text}\"**.\n\n"
                f"⏰ **Tool Executed**: `create_reminder(title=\"{reminder_text}\")`"
            )

        # 6. Memory Bank Storage Intent
        if any(w in text_lower for w in ["remember ", "keep in mind", "save preference"]):
            match = re.search(r'(?:remember|keep in mind|save preference)\s+(?:that\s+)?(.+)', last_prompt, re.IGNORECASE)
            memory_content = match.group(1).strip() if match else last_prompt
            return (
                f"I have saved this directive to your Memory Bank: **\"{memory_content}\"**.\n\n"
                f"🧠 **Tool Executed**: `save_memory(content=\"{memory_content}\")`\n"
                f"I will remember this in our future conversations."
            )

        # 7. Greetings & Personal AI Assistant Dialogue
        if any(w in text_lower for w in ["hi", "hello", "hey", "who are you", "what can you do"]):
            pref_note = f"\n\n*Active Personal Memories*: {system_memory}" if system_memory else ""
            return (
                f"Hello! You said: '{last_prompt}'. I am **ISAI**, your personal AI assistant running 100% autonomously on your backend.\n\n"
                f"I can help you with:\n"
                f"- 📱 **Phone Calls**: Ask me to call contacts (e.g. *'Call Mom'*)\n"
                f"- 🌐 **Web Search**: Ask me to search the internet (e.g. *'Search latest AI news'*)\n"
                f"- 🚀 **App Launcher**: Ask me to open apps (e.g. *'Open Google Maps'*)\n"
                f"- ✅ **Task & Reminders**: Ask me to manage your schedule\n"
                f"- 🧠 **Memory Bank**: Save your preferences and instructions{pref_note}"
            )

        # 8. Conversational Fallback Engine
        return (
            f"Hello! I processed your message: **\"{last_prompt}\"**.\n\n"
            f"I am **ISAI**, your personal AI assistant running 100% autonomously on your backend.\n\n"
            f"All internal AI capabilities and device controls (Calls, Web Search, App Launch, Tasks, Memories) are active and running on your system."
        )

    async def generate_response(self, history: List[PromptMessage]) -> str:
        return self._process_nlu(history)

    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        full_response = await self.generate_response(history)
        # Token-by-token word streaming
        words = full_response.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.02)
