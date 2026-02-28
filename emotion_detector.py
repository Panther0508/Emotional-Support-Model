# emotion_detector.py
from textblob import TextBlob

# Mapping simple polarity and keywords to emotions
def detect_emotion(text):
    text_lower = text.lower()
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    # Keyword based detection
    if any(word in text_lower for word in ["anxious","nervous","worried","stressed"]):
        return "anxious"
    if any(word in text_lower for word in ["angry","mad","frustrated"]):
        return "angry"
    if any(word in text_lower for word in ["lonely","alone","sad","depressed"]):
        return "sad"
    if any(word in text_lower for word in ["happy","excited","joy","yay","great"]):
        return "happy"
    if any(word in text_lower for word in ["bored","meh","okay","neutral"]):
        return "neutral"
    
    # Fallback by polarity
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    else:
        return "neutral"

# Quick test
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print(f"[Detected Emotion]: {detect_emotion(user_input)}")