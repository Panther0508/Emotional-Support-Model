# chatbot.py
import json
import random
from emotion_detector import detect_emotion

# Fix: read JSON with UTF-8
with open("coping_suggestions.json", "r", encoding="utf-8") as f:
    coping = json.load(f)

# Simple personalities
personalities = {
    "empathetic": {"happy": "That's wonderful! 💛", "sad": "I'm here for you 🤗", "anxious": "Take a deep breath, I understand 💛", "angry": "It's okay to vent 😌", "neutral": "I hear you 👂"},
    "funny": {"happy": "Yay! 😎 Celebrate like a boss!", "sad": "Aw man 😢 I’d send cookies if I could 🍪", "anxious": "Don't worry, breathe like a dragon 🐉", "angry": "Calm down, Hulk 🟢", "neutral": "Meh, life, right? 😏"},
    "motivational": {"happy": "Keep shining! 🌟", "sad": "You can overcome this 💪", "anxious": "Focus, breathe, conquer 💥", "angry": "Turn that fire into fuel 🔥", "neutral": "Every moment is a chance 🌱"}
}

def get_response(user_input, personality="empathetic"):
    emotion = detect_emotion(user_input)
    response = personalities.get(personality, personalities["empathetic"]).get(emotion)
    
    # Add coping tip for negative emotions
    if emotion in ["sad","anxious","angry"]:
        tip = random.choice(coping.get(emotion, ["Take a deep breath 💛"]))
        response += " | Tip: " + tip
    
    return response, emotion