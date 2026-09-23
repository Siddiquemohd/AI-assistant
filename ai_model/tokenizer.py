import json

class CustomTokenizer:
    """
    Byte/Character-level Tokenizer built from scratch for training a custom LLM.
    """
    def __init__(self):
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"
        self.bos_token = "<BOS>"
        self.eos_token = "<EOS>"
        
        self.special_tokens = [self.pad_token, self.unk_token, self.bos_token, self.eos_token]
        
        self.char2idx = {tok: idx for idx, tok in enumerate(self.special_tokens)}
        self.idx2char = {idx: tok for idx, tok in enumerate(self.special_tokens)}

    def build_vocab(self, texts: list[str]):
        unique_chars = sorted(list(set("".join(texts))))
        for char in unique_chars:
            if char not in self.char2idx:
                idx = len(self.char2idx)
                self.char2idx[char] = idx
                self.idx2char[idx] = char

    @property
    def vocab_size(self) -> int:
        return len(self.char2idx)

    def encode(self, text: str, add_special_tokens: bool = True) -> list[int]:
        tokens = []
        if add_special_tokens:
            tokens.append(self.char2idx[self.bos_token])
        
        for char in text:
            tokens.append(self.char2idx.get(char, self.char2idx[self.unk_token]))

        if add_special_tokens:
            tokens.append(self.char2idx[self.eos_token])
            
        return tokens

    def decode(self, token_ids: list[int]) -> str:
        chars = []
        for idx in token_ids:
            char = self.idx2char.get(idx, "")
            if char not in self.special_tokens:
                chars.append(char)
        return "".join(chars)

    def save(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"char2idx": self.char2idx}, f, indent=2)

    def load(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.char2idx = data["char2idx"]
            self.idx2char = {int(v): k for k, v in self.char2idx.items()}
