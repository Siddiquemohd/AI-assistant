import torch
import torch.nn.functional as F
from model import CustomLLMFromScratch
from tokenizer import CustomTokenizer

def generate_text(model, tokenizer, prompt: str, max_new_tokens: int = 100, temperature: float = 0.7, top_k: int = 10, device: str = "cpu") -> str:
    model.eval()
    token_ids = tokenizer.encode(prompt, add_special_tokens=False)
    input_ids = torch.tensor([token_ids], dtype=torch.long, device=device)

    for _ in range(max_new_tokens):
        # Truncate to max sequence length if needed
        input_cond = input_ids[:, -model.max_seq_len:]
        
        with torch.no_grad():
            logits, _ = model(input_cond)
            # Focus only on the last time step
            logits = logits[:, -1, :] / temperature

            # Top-K Sampling
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = -float('Inf')

            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)

            input_ids = torch.cat((input_ids, next_token), dim=1)

            # Break if EOS token encountered
            if next_token.item() == tokenizer.char2idx[tokenizer.eos_token]:
                break

    output_token_ids = input_ids[0].tolist()
    return tokenizer.decode(output_token_ids)

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    tokenizer = CustomTokenizer()
    tokenizer.load("checkpoint/tokenizer.json")

    model = CustomLLMFromScratch(
        vocab_size=tokenizer.vocab_size,
        d_model=256,
        n_layers=4,
        n_heads=4,
        max_seq_len=64
    ).to(device)

    model.load_state_dict(torch.load("checkpoint/custom_llm_model.pt", map_location=device))
    print("Custom AI Model loaded successfully!")

    prompt = "def hello_world():"
    generated = generate_text(model, tokenizer, prompt, max_new_tokens=80, device=device)
    print(f"\n--- Prompt ---\n{prompt}")
    print(f"\n--- Generated Output ---\n{generated}")
