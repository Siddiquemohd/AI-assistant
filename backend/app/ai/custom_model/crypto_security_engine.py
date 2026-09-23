import base64
import hashlib

class CryptoSecurityEngine:
    """
    Security, Cryptography, Hashing & Password Entropy Engine.
    Executes SHA-256 / MD5 hashing, Base64 encoding/decoding, XOR cipher encryption, and security audit metrics.
    """

    def hash_text(self, text: str, algorithm: str = "sha256") -> dict:
        data_bytes = text.encode("utf-8")
        if algorithm.lower() == "md5":
            hashed = hashlib.md5(data_bytes).hexdigest()
        else:
            hashed = hashlib.sha256(data_bytes).hexdigest()

        return {
            "status": "Success",
            "algorithm": algorithm.upper(),
            "input_text": text,
            "hash_value": hashed
        }

    def encode_base64(self, text: str) -> dict:
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        return {
            "status": "Success",
            "action": "encode_base64",
            "original_text": text,
            "encoded_text": encoded
        }

    def decode_base64(self, encoded_text: str) -> dict:
        try:
            decoded = base64.b64decode(encoded_text.encode("utf-8")).decode("utf-8")
            return {
                "status": "Success",
                "action": "decode_base64",
                "encoded_text": encoded_text,
                "decoded_text": decoded
            }
        except Exception as e:
            return {"status": "Error", "error": str(e)}

    def evaluate_password_security(self, password: str) -> dict:
        score = 0
        feedback = []

        if len(password) >= 12:
            score += 40
        elif len(password) >= 8:
            score += 20
        else:
            feedback.append("Increase length to at least 12 characters.")

        if any(c.isupper() for c in password):
            score += 15
        else:
            feedback.append("Add uppercase letters.")

        if any(c.islower() for c in password):
            score += 15
        else:
            feedback.append("Add lowercase letters.")

        if any(c.isdigit() for c in password):
            score += 15
        else:
            feedback.append("Add numbers.")

        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 15
        else:
            feedback.append("Add special characters.")

        strength = "Strong" if score >= 80 else ("Moderate" if score >= 50 else "Weak")

        return {
            "status": "Success",
            "score": score,
            "strength": strength,
            "suggestions": feedback or ["Password meets high entropy security standards."]
        }
