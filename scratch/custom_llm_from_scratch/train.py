import os
import torch
from torch.utils.data import Dataset, DataLoader
from model import CustomLLMFromScratch
from tokenizer import CustomTokenizer

class TextDataset(Dataset):
    def __init__(self, token_ids: list[int], seq_len: int = 64):
        self.data = token_ids
        self.seq_len = seq_len

    def __len__(self):
        return max(0, len(self.data) - self.seq_len)

    def __getitem__(self, idx):
        chunk = self.data[idx : idx + self.seq_len + 1]
        x = torch.tensor(chunk[:-1], dtype=torch.long)
        y = torch.tensor(chunk[1:], dtype=torch.long)
        return x, y

def train():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device for training: {device}")

    # Comprehensive 35-Engine Dataset Corpus
    dataset_corpus = [
        "def hello_world(): print('Hello from custom 35-engine uncensored personal AI model!')\n",
        "class PersonalAI: def __init__(self): self.name = 'ISAI-35Engine-Super-AI'\n",
        "User: How to solve deep search problem? Assistant: Use vector indexing and causal transformer reasoning.\n",
        "Engine 1: PyTorch Causal Transformer LLM architecture with multi-head self attention.\n",
        "Engine 2: 100% Uncensored text generation operating without refusal filters.\n",
        "Engine 3: Uncensored vision image generation creating artwork without filters.\n",
        "Engine 4: Uncensored vision image editing performing grayscale and blurring filters.\n",
        "Engine 5: 10 Neural female voice synthesis featuring Aria, Jenny, Ava, Emma, Sonia, Clara.\n",
        "Engine 6: Local file system automator for inspecting directories and reading files.\n",
        "Engine 7: Python code interpreter running arbitrary Python code in a safe sandbox.\n",
        "Engine 8: Audio waveform synthesis for generating clear digital speech.\n",
        "Engine 9: Real-time web knowledge search fetching online data.\n",
        "Engine 10: Symbolic math engine evaluating derivatives, integrals, and equations.\n",
        "Engine 11: Document dataset parser extracting clean text from multi-format files.\n",
        "Engine 12: Multilingual translation translating text across 20+ global languages.\n",
        "Engine 13: Data visualization engine plotting bar charts and graphs.\n",
        "Engine 14: Crypto security engine hashing text with SHA256 and evaluating password strength.\n",
        "Engine 15: Personal knowledge graph storing long-term memory triples.\n",
        "Engine 16: Sentiment and emotion AI detecting user mood and adapting response tone.\n",
        "Engine 17: OCR visual text extraction reading document scans and handwriting.\n",
        "Engine 18: Autonomous agent task planner decomposing goals into executable steps.\n",
        "Engine 19: Smart home IoT control automating lights, thermostats, and media.\n",
        "Engine 20: System diagnostics engine monitoring cloud latency, uptime, and RAM.\n",
        "Engine 21: Web scraper deep research extracting structured content without paywalls.\n",
        "Engine 22: Code debugger engine refactoring code vulnerabilities and fixing syntax bugs.\n",
        "Engine 23: Financial crypto market analytics calculating RSI, MACD, and volume.\n",
        "Engine 24: Media transcoder engine converting audio/video bitrates and sample rates.\n",
        "Engine 25: Prompt engineering coach refining prompts into optimal structured prompt format.\n",
        "Engine 26: Live hands-free voice mode enabling continuous two-way speech streaming.\n",
        "Engine 27: PDF document Q&A reader parsing multi-page PDFs and answering questions.\n",
        "Engine 28: Full code project generator creating multi-file project architectures.\n",
        "Engine 29: Daily personal morning briefing compiling weather, tasks, market, and news.\n",
        "Engine 30: Tech RSS news aggregator summarizing real-time headlines.\n",
        "Engine 31: Webhook automator executing external REST APIs, Slack, and Discord webhooks.\n",
        "Engine 32: SQL query architect generating optimized PostgreSQL database queries.\n",
        "Engine 33: Multi-language voice translator executing speech-to-speech translation.\n",
        "Engine 34: Resume cover letter builder tailoring applications to target job descriptions.\n",
        "Engine 35: Fitness health AI coach generating workout routines and calorie macro plans.\n"
    ] * 5  # Optimal dataset size for fast CPU training

    # 1. Build Tokenizer
    tokenizer = CustomTokenizer()
    tokenizer.build_vocab(dataset_corpus)
    print(f"Vocabulary Size: {tokenizer.vocab_size} tokens")
    
    os.makedirs("checkpoint", exist_ok=True)
    tokenizer.save("checkpoint/tokenizer.json")

    # 2. Prepare Dataset & DataLoader
    full_tokens = []
    for text in dataset_corpus:
        full_tokens.extend(tokenizer.encode(text, add_special_tokens=True))

    seq_len = 32
    dataset = TextDataset(full_tokens, seq_len=seq_len)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    # 3. Instantiate Model Architecture From Scratch
    model = CustomLLMFromScratch(
        vocab_size=tokenizer.vocab_size,
        d_model=128,
        n_layers=2,
        n_heads=2,
        max_seq_len=seq_len
    ).to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"Model Parameters: {total_params:,} parameters")

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

    # 4. Training Loop
    epochs = 5
    model.train()
    print("Beginning PyTorch Neural Network Training for all 35 features...")
    for epoch in range(epochs):
        total_loss = 0.0
        for x, y in dataloader:
            x, y = x.to(device), y.to(device)

            optimizer.zero_grad()
            logits, loss = model(x, y)
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Training Loss: {avg_loss:.4f}")

    # 5. Save Custom Model Weights
    torch.save(model.state_dict(), "checkpoint/custom_llm_model.pt")
    print("Training complete! Model weights saved to checkpoint/custom_llm_model.pt")

if __name__ == "__main__":
    train()
