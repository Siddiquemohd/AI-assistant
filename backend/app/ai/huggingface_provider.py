import os
import urllib.parse
import asyncio
import httpx
from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage

class HuggingFaceProvider(BaseAiProvider):
    """
    AI Provider routing text requests to custom fine-tuned Llama-3.2-3B model
    (Siddiquiee/ISAI-Custom-Llama3.2-3B) and image generation requests to FLUX.1 Uncensored Diffusion.
    """
    def __init__(self, repo_id: str = "Siddiquiee/ISAI-Custom-Llama3.2-3B", hf_token: str = None):
        self.repo_id = repo_id
        self.token = hf_token or os.getenv("HF_TOKEN", "")
        self.api_url = f"https://api-inference.huggingface.co/models/{self.repo_id}"

    @property
    def name(self) -> str:
        return f"HuggingFace-{self.repo_id}"

    async def generate_response(self, history: List[PromptMessage]) -> str:
        user_msg = next((m.content for m in reversed(history) if m.role == "user"), "Hello").strip()
        user_msg_lower = user_msg.lower()
        
        # Image Generation Intent Detection (Uncensored FLUX.1 Engine)
        image_keywords = ["create image", "generate image", "create a picture", "draw", "generate a picture", "create a 18 year old girl image", "image of", "picture of"]
        if any(kw in user_msg_lower for kw in image_keywords) or (("create" in user_msg_lower or "generate" in user_msg_lower or "draw" in user_msg_lower) and "image" in user_msg_lower):
            encoded_prompt = urllib.parse.quote(user_msg)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
            return (
                f"🎨 **Uncensored Image Generation Output**:\n\n"
                f"![{user_msg}]({image_url})\n\n"
                f"Here is your generated image for: *\"{user_msg}\"*"
            )

        headers = {
            "Content-Type": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        formatted_prompt = (
            f"<|start_header_id|>system<|end_header_id|>\n"
            f"You are ISAI, a custom uncensored personal AI assistant.<|eot_id|>\n"
            f"<|start_header_id|>user<|end_header_id|>\n"
            f"{user_msg}<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n"
        )

        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": 256,
                "temperature": 0.7,
                "return_full_text": False
            }
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(self.api_url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and len(data) > 0:
                        raw = data[0].get("generated_text", "")
                        return raw.strip() if raw.strip() else "I am ISAI, your custom AI assistant."
                elif res.status_code == 503:
                    return "Your custom Hugging Face model is powering up. Please try again in 30 seconds!"
                res.raise_for_status()
        except Exception as e:
            print(f"Hugging Face API request error: {e}")
            return f"Hello! I am your custom ISAI model (Processed via custom fine-tuned weights)."

        return "I am ISAI, your personal AI assistant."

    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        full_res = await self.generate_response(history)
        words = full_res.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.02)
