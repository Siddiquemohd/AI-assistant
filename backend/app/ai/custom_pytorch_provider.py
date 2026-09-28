import os
import asyncio
import torch
from typing import AsyncGenerator, List
from app.ai.base import BaseAiProvider, PromptMessage
from app.ai.custom_model.model import CustomLLMFromScratch
from app.ai.custom_model.tokenizer import CustomTokenizer
from app.ai.custom_model.generate import generate_text
from app.ai.custom_model.multimodal_assistant import MultimodalPersonalAI

class CustomPyTorchProvider(BaseAiProvider):
    """
    Custom PyTorch AI Provider loading checkpoint/custom_llm_model.pt
    and MultimodalPersonalAI engine.
    """
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = CustomTokenizer()
        
        # Determine path to checkpoint directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        checkpoint_dir = os.path.join(base_dir, "checkpoint")
        
        tokenizer_path = os.path.join(checkpoint_dir, "tokenizer.json")
        model_path = os.path.join(checkpoint_dir, "custom_llm_model.pt")

        if os.path.exists(tokenizer_path):
            try:
                self.tokenizer.load(tokenizer_path)
            except Exception as e:
                print(f"Error loading tokenizer: {e}")

        self.model = None
        if os.path.exists(model_path):
            try:
                state_dict = torch.load(model_path, map_location=self.device)
                vocab_size = state_dict["token_emb.weight"].shape[0] if "token_emb.weight" in state_dict else getattr(self.tokenizer, "vocab_size", 40)
                self.model = CustomLLMFromScratch(
                    vocab_size=vocab_size,
                    d_model=256,
                    n_layers=4,
                    n_heads=4,
                    max_seq_len=64
                ).to(self.device)
                self.model.load_state_dict(state_dict)
                self.model.eval()
                print("Successfully loaded custom_llm_model.pt into PyTorch Provider!")
            except Exception as e:
                print(f"Error loading custom_llm_model.pt: {e}")
                self.model = None

        self.multimodal_assistant = MultimodalPersonalAI()

    @property
    def name(self) -> str:
        return "CustomPyTorch-LLM-Engine"

    async def generate_response(self, history: List[PromptMessage]) -> str:
        user_messages = [m.content for m in history if m.role == "user"]
        if not user_messages:
            return "Hello! I am your Custom PyTorch AI Model."
        
        last_prompt = user_messages[-1].strip()

        # Execute custom PyTorch model generation if available
        if self.model is not None and len(last_prompt) > 0:
            try:
                generated_text = generate_text(
                    self.model,
                    self.tokenizer,
                    prompt=last_prompt[:30],
                    max_new_tokens=60,
                    device=self.device
                )
                if generated_text and len(generated_text.strip()) > len(last_prompt):
                    return generated_text
            except Exception as e:
                print(f"PyTorch model generation fallback: {e}")

        # Process through multimodal assistant engine suite
        res_dict = self.multimodal_assistant.process(last_prompt)
        return res_dict.get("response", "Processing complete.")

    async def stream_response(self, history: List[PromptMessage]) -> AsyncGenerator[str, None]:
        full_response = await self.generate_response(history)
        words = full_response.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.02)
