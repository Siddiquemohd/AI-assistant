import os
import torch
from torch.utils.data import Dataset, DataLoader
from model import CustomLLMFromScratch
from tokenizer import CustomTokenizer

class TextDataset(Dataset):
    def __init__(self, token_ids: list[int], seq_len: int = 128):
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
    print(f"Using device for training from scratch: {device}")

    # Sample raw text dataset (Python code + Deep research text + Conversations)
    dataset_corpus = [
        "def hello_world(): print('Hello from my custom personal AI model built from scratch!')\n",
        "class PersonalAI: def __init__(self): self.name = 'ISAI-Scratch'\n",
        "User: How to solve deep search problem? Assistant: Use vector indexing, graph embeddings, and causal transformer reasoning.\n",
        "Python is a powerful programming language used for neural networks, artificial intelligence, and software engineering.\n",
        "To build a model from scratch, write PyTorch Multi-Head Self-Attention, RMSNorm, SwiGLU Feed-Forward Networks, and AdamW optimization.\n"
    ] * 50  # Replicate for training iterations

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

    seq_len = 64
    dataset = TextDataset(full_tokens, seq_len=seq_len)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    # 3. Instantiate Model Architecture From Scratch
    model = CustomLLMFromScratch(
        vocab_size=tokenizer.vocab_size,
        d_model=256,
        n_layers=4,
        n_heads=4,
        max_seq_len=seq_len
    ).to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"Model Parameters: {total_params:,} parameters")

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

    # 4. Training Loop (Cross Entropy Loss & Gradient Clipping)
    epochs = 15
    model.train()
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
        print(f"Epoch [{epoch+1}/{epochs}] | Loss: {avg_loss:.4f}")

    # 5. Save Custom Model Weights
    torch.save(model.state_dict(), "checkpoint/custom_llm_model.pt")
    print("Training complete! Model saved to checkpoint/custom_llm_model.pt")

if __name__ == "__main__":
    train()
