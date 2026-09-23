import os
import asyncio
import edge_tts

class UltraRealisticVoiceEngine:
    """
    Ultra-Realistic Female Voice Engine.
    Provides 10+ distinct sweet, alluring, and natural female neural voices for AI speech synthesis.
    """

    FEMALE_VOICES = {
        "aria": {
            "id": "en-US-AriaNeural",
            "name": "Aria (US English - Sweet & Natural)",
            "style": "sweet, expressive, alluring"
        },
        "jenny": {
            "id": "en-US-JennyNeural",
            "name": "Jenny (US English - Soft & Friendly)",
            "style": "soft, warm, friendly"
        },
        "ava": {
            "id": "en-US-AvaNeural",
            "name": "Ava (US English - Deep & Smooth)",
            "style": "deep, smooth, captivating"
        },
        "emma": {
            "id": "en-US-EmmaNeural",
            "name": "Emma (US English - Warm & Engaging)",
            "style": "warm, melodic, engaging"
        },
        "sonia": {
            "id": "en-UK-SoniaNeural",
            "name": "Sonia (British English - Elegant & Melodic)",
            "style": "elegant, refined, melodic"
        },
        "clara": {
            "id": "en-CA-ClaraNeural",
            "name": "Clara (Canadian English - Gentle & Soft)",
            "style": "gentle, soft, alluring"
        },
        "natasha": {
            "id": "en-AU-NatashaNeural",
            "name": "Natasha (Australian English - Charming & Smooth)",
            "style": "charming, warm, smooth"
        },
        "neerja": {
            "id": "en-IN-NeerjaNeural",
            "name": "Neerja (Indian English - Expressive & Soft)",
            "style": "expressive, sweet, soft"
        },
        "elvira": {
            "id": "es-ES-ElviraNeural",
            "name": "Elvira (Spanish - Passionate & Soft)",
            "style": "passionate, smooth, soft"
        },
        "denise": {
            "id": "fr-FR-DeniseNeural",
            "name": "Denise (French - Silky & Alluring)",
            "style": "silky, elegant, alluring"
        }
    }

    def list_voices(self) -> list[dict]:
        return [
            {"key": k, "name": v["name"], "style": v["style"], "voice_id": v["id"]}
            for k, v in self.FEMALE_VOICES.items()
        ]

    async def speak_async(self, text: str, voice_key: str = "aria", pitch: str = "+0Hz", rate: str = "+0%", output_path: str = "output_speech.mp3") -> dict:
        voice_key_clean = voice_key.lower().strip()
        voice_info = self.FEMALE_VOICES.get(voice_key_clean, self.FEMALE_VOICES["aria"])
        voice_id = voice_info["id"]

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

        communicate = edge_tts.Communicate(text, voice_id, pitch=pitch, rate=rate)
        await communicate.save(output_path)

        return {
            "status": "Success",
            "voice_name": voice_info["name"],
            "voice_style": voice_info["style"],
            "pitch": pitch,
            "rate": rate,
            "file_path": output_path
        }

    def speak(self, text: str, voice_key: str = "aria", pitch: str = "+0Hz", rate: str = "+0%", output_path: str = "output_speech.mp3") -> dict:
        return asyncio.run(self.speak_async(text, voice_key, pitch, rate, output_path))
