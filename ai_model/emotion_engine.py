"""
Sentiment, Mood & Emotional Intelligence Engine for ISAI Personal AI.
Analyzes user intent emotional tone and generates empathetic adaptive responses.
"""
from typing import Dict, Any

class EmotionIntelligenceEngine:
    def __init__(self):
        self.emotion_keywords = {
            "joy": ["happy", "excited", "awesome", "great", "love", "amazing", "wonderful", "yay"],
            "sadness": ["sad", "depressed", "lonely", "upset", "unhappy", "cry", "miserable"],
            "anger": ["angry", "furious", "mad", "hate", "frustrated", "annoyed"],
            "stress": ["stressed", "overwhelmed", "anxious", "worried", "nervous", "busy"],
            "curiosity": ["how", "why", "what if", "explain", "learn", "wonder", "curious"]
        }

    def detect_emotion(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        scores = {emotion: 0 for emotion in self.emotion_keywords}
        
        for emotion, keywords in self.emotion_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[emotion] += 1
                    
        primary_emotion = max(scores, key=scores.get)
        confidence = scores[primary_emotion]
        
        if confidence == 0:
            primary_emotion = "neutral"
            
        adaptive_tone = {
            "joy": "enthusiastic, cheerful, warm",
            "sadness": "empathetic, comforting, supportive",
            "anger": "calm, reassuring, polite",
            "stress": "soothing, structured, helpful",
            "curiosity": "insightful, detailed, engaging",
            "neutral": "friendly, balanced, professional"
        }.get(primary_emotion, "friendly")
        
        return {
            "detected_emotion": primary_emotion,
            "confidence_score": confidence,
            "recommended_tone": adaptive_tone,
            "voice_pitch_shift": "+10%" if primary_emotion in ["joy", "curiosity"] else "-5%" if primary_emotion in ["sadness", "stress"] else "0%"
        }
