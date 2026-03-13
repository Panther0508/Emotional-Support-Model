# chatbot.py - Chatbot Logic for Emotional Support AI
import json
import random
import os
from datetime import datetime
from emotion_detector import (
    detect_emotion, 
    get_emotion_emoji, 
    analyze_emotions,
    get_dominant_emotion,
    is_crisis_keywords,
    get_crisis_response
)

# Load coping suggestions
def load_coping_suggestions():
    """Load coping suggestions from file with fallback"""
    try:
        with open("coping_suggestions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "sad": [
                "Take a deep breath and think of one thing you're grateful for",
                "Go for a short walk to get some fresh air",
                "Write down what you're feeling - it can help process emotions",
                "Listen to your favorite calming music",
                "Reach out to someone you trust - you don't have to face this alone"
            ],
            "anxious": [
                "Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste",
                "Practice box breathing: Inhale 4 sec, hold 4 sec, exhale 4 sec, hold 4 sec",
                "Write down what's worrying you to get it out of your head",
                "Take a warm shower or bath to relax your muscles",
                "Do some light stretching to release physical tension"
            ],
            "angry": [
                "Count to 10 slowly before responding",
                "Take a walk or do some physical exercise",
                "Listen to calming music or nature sounds",
                "Journal about what's making you angry",
                "Squeeze a stress ball or punch a pillow (safely)"
            ],
            "neutral": [
                "Take a moment to reflect on your day",
                "Drink some water and stretch",
                "Consider what small step you could take toward a goal",
                "Practice gratitude by listing three good things"
            ],
            "happy": [
                "Share your happiness with someone you care about",
                "Take a moment to savor this feeling",
                "Consider doing something nice for others"
            ]
        }

coping_suggestions = load_coping_suggestions()

# Load training data for intent matching
def load_training_data():
    """Load training data from file with fallback"""
    try:
        with open("training_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"intents": [], "emotions": {}}

training_data = load_training_data()

# Enhanced personality responses with more variety
personalities = {
    "empathetic": {
        "happy": [
            "That's wonderful! I'm so happy for you! 💛",
            "Your joy really shines through! That's beautiful to hear! 🌟",
            "I'm thrilled to hear that! You deserve all the happiness! 🎉"
        ],
        "sad": [
            "I'm here for you. It seems like you're going through a difficult time. 🤗",
            "I can hear how much this is affecting you. Thank you for sharing with me. 💙",
            "It's okay to feel sad. Your feelings are valid, and I'm here to listen. 🌸",
            "I'm so sorry you're going through this. You're not alone. 🤍"
        ],
        "anxious": [
            "Take a deep breath. I understand this feels overwhelming. 💛",
            "It's completely natural to feel anxious. Let's work through this together. 🫂",
            "I hear you. Whatever you're facing, you have the strength to get through it. 💙",
            "Take it one step at a time. I'm right here with you. 🌿"
        ],
        "angry": [
            "It's completely okay to feel angry. Let it out, I'm listening. 😌",
            "Your feelings are valid. It's okay to feel this way. 🤍",
            "I hear you - this sounds really frustrating. I'm here to support you. 💙",
            "Being angry is a natural response to difficult situations. Let's talk about it. 🌸"
        ],
        "neutral": [
            "I hear you. Tell me more about what's on your mind. 👂",
            "I'm here to listen. What's been on your heart lately? 💭",
            "Thank you for sharing this moment with me. I'm all ears. 🌟"
        ]
    },
    "funny": {
        "happy": [
            "Yay! That's awesome! 😎 Celebrate like a boss!",
            "Woohoo! You're glowing! ✨ Time to do the happy dance!",
            "That's amazing news! I literally cannot contain my excitement! 🎉"
        ],
        "sad": [
            "Aw man, I'm sorry 😢 I'd send cookies if I could 🍪",
            "Hey, it's okay to be sad. Even robots get the blues sometimes 🤖💙",
            "I wish I could give you a giant hug right now 🫂 Cookie for your thoughts? 🍪"
        ],
        "anxious": [
            "Don't worry, breathe like a dragon 🐉 You've got this!",
            "Hey, let's tackle this one worry at a time! 📝 Baby steps! 🚶",
            "I believe in you! You're stronger than you think! 💪🌟"
        ],
        "angry": [
            "Calm down, Hulk 🟢 Take it easy, friend!",
            "I get it - sometimes life is like a bad joke 😤 But you've got this!",
            "Let it out! Sometimes that's the first step to feeling better 💙"
        ],
        "neutral": [
            "Meh, life, right? 😏 But hey, I'm here for you!",
            "Alrighty then! What's the scoop? 📰 I'm all ears! 👂",
            "Hey, thanks for hanging out with me! 💛 What's on your mind?"
        ]
    },
    "motivational": {
        "happy": [
            "Keep shining! Your positivity is inspiring! 🌟",
            "This is your moment! Embrace it fully! 💫",
            "Your joy is contagious! Let it fuel your next adventure! 🚀"
        ],
        "sad": [
            "You can overcome this challenge. I believe in you! 💪",
            "This is just a chapter, not your whole story. Better days are ahead! 📖✨",
            "Your strength is greater than your struggle. Keep going! 🌅",
            "Every storm runs out of rain. Stay hopeful! ☀️"
        ],
        "anxious": [
            "Focus, breathe, conquer! You're stronger than your fears! 💥",
            "One breath at a time. One step at a time. You've got this! 🏔️",
            "Your potential is limitless! Don't let anxiety hold you back! 🚀",
            "Transform fear into fuel! You've overcome challenges before, and you'll do it again! 💪"
        ],
        "angry": [
            "Turn that fire into fuel! Channel your energy positively! 🔥",
            "Use this energy to drive change! You're powerful! ⚡",
            "Your anger shows you care. Now let's harness it for something great! 💪🌟"
        ],
        "neutral": [
            "Every moment is a chance to grow. Make it count! 🌱",
            "The best time to start is now. What will you accomplish today? ⭐",
            "Your journey is just beginning. Dream big and act now! 🚀"
        ]
    },
    "calm": {
        "happy": [
            "Your joy brings warmth to this conversation. 😊",
            "It's wonderful to share this moment of happiness with you. 🌸",
            "Your smile is contagious. Thank you for brightening my day! ✨"
        ],
        "sad": [
            "I'm listening. Take your time to share what's in your heart. 🌸",
            "It's okay to feel whatever you're feeling. I'm here, unhurried. 💙",
            "Breathe slowly. Let your feelings come and go like waves. 🌊",
            "You don't have to rush. I'm here to sit with you in this moment. 🤍"
        ],
        "anxious": [
            "Let's breathe together. In for 4, hold for 4, out for 4. 🧘",
            "Peace begins with a single breath. You are safe right now. 🌿",
            "Release the tension. Everything will be okay. Take your time. 🕊️",
            "Let's find our calm together. One breath at a time. 🧘‍♀️"
        ],
        "angry": [
            "Peace begins with a calm mind. I'm here to support you. 🕊️",
            "Take a moment to center yourself. Your peace matters. 🌸",
            "Let's find stillness together. You are stronger than your anger. 💙"
        ],
        "neutral": [
            "Thank you for sharing this moment with me. 🌿",
            "I'm here, present with you. What would feel good to talk about? 💭",
            "This quiet moment is precious. I'm glad you're here. ✨"
        ]
    }
}


def match_intent(user_input):
    """Match user input to training data intents"""
    user_input_lower = user_input.lower()
    
    for intent in training_data.get("intents", []):
        for pattern in intent.get("patterns", []):
            if pattern.lower() in user_input_lower:
                responses = intent.get("responses", [])
                if responses:
                    return random.choice(responses)
    
    return None


def get_greeting_response():
    """Get random greeting response"""
    greetings = [
        "Hello! It's so nice to see you. How are you feeling today? 💛",
        "Hey there! I'm here to chat. What's on your mind? 🌟",
        "Welcome back! It's great to have you here. How are you doing? 💙",
        "Hi! I'm ready to listen. What's going on with you today? 🌸"
    ]
    return random.choice(greetings)


def get_farewell_response():
    """Get random farewell response"""
    farewells = [
        "Take care of yourself! Remember, I'm always here when you need me. 💛",
        "Goodbye, friend! Until next time. You've got this! 🌟",
        "It was great chatting with you! Stay strong and keep going! 💙",
        "Bye for now! Don't forget - you're amazing and loved! 🌸"
    ]
    return random.choice(farewells)


def get_random_encouragement():
    """Get random encouraging message"""
    encouragements = [
        "You're doing great! Keep being honest with yourself. 💛",
        "I appreciate you sharing this with me. You're brave! 🌟",
        "Remember, it's okay to feel whatever you're feeling. 💙",
        "You're not alone in this. I'm here for you. 🌸",
        "Every conversation is a step forward. Be proud of yourself! 💪"
    ]
    return random.choice(encouragements)


def get_response(user_input, personality="empathetic"):
    """
    Get AI response based on user input and personality using external APIs.
    
    Args:
        user_input: The user's message
        personality: The selected AI personality (empathetic, funny, motivational, calm)
    
    Returns:
        tuple: (response_message, detected_emotion)
    """
    user_input_clean = user_input.strip()
    
    # 1. Check for crisis keywords first (immediate priority)
    if is_crisis_keywords(user_input_clean):
        return get_crisis_response(), "sad"  # Return crisis response with sad emotion
    
    # Detect emotion from input for context
    emotion = detect_emotion(user_input_clean)
    
    # 2. Get AI personality description for system prompting
    personality_info = get_personality_description(personality)
    system_instruction = (
        f"You are an emotional support AI. Your personality is '{personality}'. "
        f"Description: {personality_info}. "
        f"IMPORTANT: Always respond in English only, regardless of the language used by the user. "
        f"Never respond in Chinese or any other language. Keep responses concise and caring."
    )
    if emotion and emotion != "neutral":
        system_instruction += f"The user seems to be feeling {emotion}. Please respond accordingly with extreme empathy and care."
        
    # Import the API clients
    from apis.api_config import get_config
    from apis.google_ai import GoogleAIClient, GoogleAIError
    from apis.huggingface_api import HuggingFaceClient, HuggingFaceError
    
    config = get_config()
    response = None
    
    # 3. Try Google AI (Gemini) First
    if config.is_google_configured:
        try:
            google_client = GoogleAIClient(config)
            response = google_client.generate_text(
                prompt=user_input_clean,
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=300
            )
        except Exception as e:
            print(f"Google AI Error: {e}")
            response = None
            
    # 4. Try Hugging Face if Google AI fails or isn't configured
    if not response and config.is_hf_configured:
        try:
            hf_client = HuggingFaceClient(config)
            hf_prompt = f"System: {system_instruction}\nUser: {user_input_clean}\nSupportive AI Response:"
            response = hf_client.generate_text(
                prompt=hf_prompt,
                max_new_tokens=300,
                temperature=0.7
            )
        except Exception as e:
            print(f"Hugging Face Error: {e}")
            response = None

    # 5. Local Fallback logic if both APIs fail or aren't configured
    if not response:
        print("Falling back to local static responses.")
        intent_response = match_intent(user_input_clean)
        if intent_response:
            response = intent_response
        else:
            personality_responses = personalities.get(personality, personalities["empathetic"])
            base_responses = personality_responses.get(emotion, personality_responses["neutral"])
            response = random.choice(base_responses)

    # Add coping tip for negative emotions (unless it's a crisis response)
    if emotion in ["sad", "anxious", "angry"] and not is_crisis_keywords(user_input_clean):
        tips = coping_suggestions.get(emotion, ["Take a deep breath"])
        tip = random.choice(tips)
        response = f"{response}\n\n💡 Tip: {tip}"
    
    return response, emotion


def get_personalities():
    """Return list of available personalities"""
    return list(personalities.keys())


def get_personality_description(personality):
    """Get description of a personality"""
    descriptions = {
        "empathetic": "Understanding and empathetic conversation style, listening patiently to your feelings.",
        "funny": "Light-hearted and humorous conversation style, using laughter to ease negative emotions.",
        "motivational": "Inspirational and encouraging conversation style, helping you overcome challenges.",
        "calm": "Peaceful and gentle conversation style, helping you relax and find tranquility."
    }
    return descriptions.get(personality, "A supportive conversation style.")


def get_personality_info():
    """Get detailed personality information"""
    return {
        "empathetic": {
            "name": "Empathetic",
            "icon": "heart",
            "description": "Understanding and patient listener who validates your feelings",
            "best_for": "Venting, seeking validation, emotional support"
        },
        "funny": {
            "name": "Funny",
            "icon": "laugh-squint",
            "description": "Light-hearted and humorous to lift your mood",
            "best_for": "Lightening mood, casual chat, easing tension"
        },
        "motivational": {
            "name": "Motivational",
            "icon": "fire",
            "description": "Encouraging and inspiring to help you overcome challenges",
            "best_for": "Seeking motivation, goal setting, encouragement"
        },
        "calm": {
            "name": "Calm",
            "icon": "spa",
            "description": "Peaceful and grounding to help you find tranquility",
            "best_for": "Anxiety relief, stress management, finding peace"
        }
    }
