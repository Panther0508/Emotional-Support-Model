# emotion_detector.py - Emotion Detection for Emotional Support AI
try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None
import re

# Enhanced keyword mappings with weights for emotion detection
EMOTION_KEYWORDS = {
    "anxious": [
        "anxious", "nervous", "worried", "stressed", "overwhelmed", "panic", "fear", "scared", 
        "afraid", "tense", "apprehensive", "uneasy", "restless", "on edge", "frightened", 
        "terrified", "horrified", "dread", "concerned", "nervousness", "anxiety"
    ],
    "angry": [
        "angry", "mad", "frustrated", "annoyed", "furious", "irritated", "hostile", "rage", 
        "hate", "outraged", "enraged", "livid", "bitter", "resentful", "infuriated", 
        "irritation", "annoyance", "fed up", "pissed", "fuming"
    ],
    "sad": [
        "sad", "unhappy", "depressed", "lonely", "alone", "miserable", "hopeless", "down", 
        "blue", "heartbroken", "devastated", "grief", "sorrow", "gloomy", "melancholy", 
        "disappointed", "hurt", "upset", "crying", "tears", "loneliness", "isolated"
    ],
    "happy": [
        "happy", "excited", "joy", "joyful", "yay", "great", "wonderful", "amazing", "love", 
        "fantastic", "glad", "delighted", "thrilled", "ecstatic", "elated", "cheerful", 
        "content", "satisfied", "grateful", "blessed", "awesome", "brilliant"
    ],
    "neutral": [
        "bored", "meh", "okay", "fine", "neutral", "alright", "whatever", "indifferent",
        "so-so", "not bad", "not good", "nothing special", "ordinary"
    ]
}

# Intensifiers that modify emotion intensity
INTENSIFIERS = ["very", "really", "extremely", "so", "super", "absolutely", "totally", "completely"]
NEGATORS = ["not", "don't", "doesn't", "didn't", "won't", "can't", "never", "no"]

# Emotion emoji mappings
EMOTION_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "anxious": "😰",
    "angry": "😠",
    "neutral": "😐"
}

# Extended emotion metadata
EMOTION_COLORS = {
    "happy": "#4CAF50",
    "sad": "#2196F3",
    "anxious": "#FF9800",
    "angry": "#F44336",
    "neutral": "#9E9E9E"
}


def preprocess_text(text):
    """Preprocess text for better analysis"""
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower().strip()
    
    # Expand contractions
    contractions = {
        "i'm": "i am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "we're": "we are",
        "they're": "they are",
        "i've": "i have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "i'll": "i will",
        "you'll": "you will",
        "he'll": "he will",
        "she'll": "she will",
        "we'll": "we will",
        "they'll": "they will",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "won't": "will not",
        "wouldn't": "would not",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "can not",
        "couldn't": "could not",
        "shouldn't": "should not",
        "mightn't": "might not",
        "mustn't": "must not"
    }
    
    for contraction, expansion in contractions.items():
        text = text.replace(contraction, expansion)
    
    return text


def detect_emotion(text):
    """
    Detect emotion from text input using keyword matching and sentiment analysis
    
    Args:
        text: User input text
    
    Returns:
        str: Detected emotion (happy, sad, anxious, angry, neutral)
    """
    if not text or not isinstance(text, str):
        return "neutral"
    
    processed_text = preprocess_text(text)
    
    # Track emotion scores
    emotion_scores = {}
    
    # Check for emotion keywords with context
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Count occurrences
            count = processed_text.count(keyword)
            if count > 0:
                # Check for intensifiers
                for intensifier in INTENSIFIERS:
                    if f"{intensifier} {keyword}" in processed_text:
                        count += 0.5  # Boost score for intensified emotions
                
                # Check for negators
                for negator in NEGATORS:
                    if f"{negator} {keyword}" in processed_text or f"{keyword} {negator}" in processed_text:
                        count -= 0.3  # Reduce score for negated emotions
                
                score += count
        
        if score > 0:
            emotion_scores[emotion] = score
    
    # If we found emotion keywords
    if emotion_scores:
        # Return the emotion with highest score
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        return primary_emotion
    
    # Fallback to sentiment analysis
    try:
        if TextBlob is None:
            return "neutral"
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        if polarity > 0.3:
            return "happy"
        elif polarity < -0.3:
            return "sad"
        elif abs(polarity) <= 0.1 and subjectivity > 0.5:
            # Low polarity but high subjectivity might indicate anxiety
            return "anxious"
        else:
            return "neutral"
    except Exception:
        return "neutral"


def get_emotion_emoji(emotion):
    """Get emoji for emotion"""
    return EMOTION_EMOJIS.get(emotion, "😐")


def get_emotion_color(emotion):
    """Get color for emotion (for UI)"""
    return EMOTION_COLORS.get(emotion, "#9E9E9E")


def analyze_emotions(text):
    """
    Analyze multiple emotions in text and return scores
    
    Args:
        text: User input text
    
    Returns:
        dict: Emotion scores (0-1 range, normalized)
    """
    if not text or not isinstance(text, str):
        return {"neutral": 1.0}
    
    processed_text = preprocess_text(text)
    scores = {}
    
    # Calculate raw scores for each emotion
    for emotion, keywords in EMOTION_KEYWORDS.items():
        raw_score = 0
        for keyword in keywords:
            count = processed_text.count(keyword)
            if count > 0:
                # Check for modifiers
                has_intensifier = any(f"{int} {keyword}" in processed_text for int in INTENSIFIERS)
                has_negator = any(f"{neg} {keyword}" in processed_text for neg in NEGATORS)
                
                if has_intensifier:
                    count *= 1.5
                if has_negator:
                    count *= 0.5
                    
                raw_score += count
        
        if raw_score > 0:
            scores[emotion] = raw_score
    
    # Normalize scores to 0-1 range
    if scores:
        total = sum(scores.values())
        scores = {k: min(v / total, 1.0) for k, v in scores.items()}
        
        # Ensure all emotions are represented
        for emotion in EMOTION_KEYWORDS:
            if emotion not in scores:
                scores[emotion] = 0.0
    else:
        # Default to neutral if no emotions detected
        scores = {emotion: 0.0 for emotion in EMOTION_KEYWORDS}
        scores["neutral"] = 1.0
    
    return scores


def get_dominant_emotion(text):
    """
    Get the dominant emotion with confidence score
    
    Args:
        text: User input text
    
    Returns:
        tuple: (emotion, confidence_score)
    """
    scores = analyze_emotions(text)
    
    if not scores or max(scores.values()) == 0:
        return ("neutral", 0.5)
    
    dominant = max(scores, key=scores.get)
    confidence = scores[dominant]
    
    return (dominant, confidence)


def is_crisis_keywords(text):
    """
    Check if text contains potential crisis indicators
    
    Args:
        text: User input text
    
    Returns:
        bool: True if crisis keywords detected
    """
    crisis_keywords = [
        "suicide", "kill myself", "end my life", "want to die",
        "self harm", "hurt myself", "cut myself",
        "overdose", "pills", "no reason to live"
    ]
    
    text_lower = text.lower() if isinstance(text, str) else ""
    
    for keyword in crisis_keywords:
        if keyword in text_lower:
            return True
    
    return False


def get_crisis_response():
    """
    Get crisis response message
    
    Returns:
        str: Crisis response with resources
    """
    return (
        "I'm really concerned about what you're sharing. It sounds like you might be going through "
        "an extremely difficult time. Please know that you don't have to face this alone.\n\n"
        "💙 If you're having thoughts of harming yourself, please reach out for immediate help:\n"
        "• National Suicide Prevention Lifeline (US): 988\n"
        "• Crisis Text Line: Text HOME to 741741\n"
        "• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/\n\n"
        "💙 Please consider talking to a trusted friend, family member, or mental health professional. "
        "You deserve support and help is available."
    )


# Quick test
if __name__ == "__main__":
    print("Emotion Detector Test")
    print("-" * 50)
    
    test_messages = [
        "I'm so happy today! Everything is amazing!",
        "I'm feeling really sad and lonely",
        "I'm so anxious about the exam next week",
        "I'm so angry at what happened to me",
        "I'm just okay, nothing special",
        "I'm not happy about this situation",
        "I'm really really scared",
        "I love you all so much!",
        "This is so frustrating and annoying",
        "I feel so alone and hopeless"
    ]
    
    for msg in test_messages:
        emotion = detect_emotion(msg)
        emoji = get_emotion_emoji(emotion)
        scores = analyze_emotions(msg)
        dominant, confidence = get_dominant_emotion(msg)
        is_crisis = is_crisis_keywords(msg)
        
        print(f"\nInput: '{msg}'")
        print(f"  Primary: {emotion} {emoji}")
        print(f"  Dominant: {dominant} ({confidence:.2f})")
        print(f"  All scores: {scores}")
        print(f"  Crisis: {is_crisis}")
