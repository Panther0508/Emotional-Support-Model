#!/usr/bin/env python
"""
API Verification Script for Emotional Support AI
This script tests the connection to Google AI and Hugging Face APIs.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set output encoding to UTF-8 for Windows compatibility
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

def test_google_ai():
    """Test Google AI API connection"""
    print("\n" + "="*60)
    print("Testing Google AI (Gemini) Connection...")
    print("="*60)
    
    try:
        from apis.api_config import get_config
        from apis.google_ai import GoogleAIClient, GoogleAIError
        
        config = get_config()
        
        if not config.is_google_configured:
            print("[X] Google AI API key not configured")
            print("    Please add GOOGLE_TOKEN to your env/.env file")
            return False
        
        print("[OK] Google AI API key found: %s..." % config.google_token[:10])
        
        # Try to create client (will validate credentials)
        try:
            client = GoogleAIClient(config)
            print("[OK] Google AI client created successfully")
        except GoogleAIError as e:
            print("[X] Google AI authentication failed: %s" % e)
            return False
        
        # Try a test request
        try:
            print("    Attempting test request...")
            response = client.generate_text(
                prompt="Say 'Hello' in a friendly way",
                max_output_tokens=50
            )
            print("[OK] Google AI Response: %s..." % response[:100])
            return True
        except GoogleAIError as e:
            print("[X] Google AI request failed: %s" % e)
            return False
            
    except ImportError as e:
        print("[X] Failed to import Google AI module: %s" % e)
        return False
    except Exception as e:
        print("[X] Unexpected error: %s" % e)
        return False


def test_huggingface():
    """Test Hugging Face API connection"""
    print("\n" + "="*60)
    print("Testing Hugging Face Connection...")
    print("="*60)
    
    try:
        from apis.api_config import get_config
        from apis.huggingface_api import HuggingFaceClient, HuggingFaceError
        
        config = get_config()
        
        if not config.is_hf_configured:
            print("[X] Hugging Face API token not configured")
            print("    Please add HF_TOKEN to your env/.env file")
            return False
        
        print("[OK] Hugging Face API token found: %s..." % config.hf_token[:10])
        
        # Try to create client (will validate credentials)
        try:
            client = HuggingFaceClient(config)
            print("[OK] Hugging Face client created successfully")
        except HuggingFaceError as e:
            print("[X] Hugging Face authentication failed: %s" % e)
            return False
        
        # Try a test request
        try:
            print("    Attempting test request...")
            response = client.generate_text(
                prompt="Say 'Hello' in a friendly way",
                max_new_tokens=50
            )
            print("[OK] Hugging Face Response: %s..." % response[:100])
            return True
        except HuggingFaceError as e:
            print("[X] Hugging Face request failed: %s" % e)
            return False
            
    except ImportError as e:
        print("[X] Failed to import Hugging Face module: %s" % e)
        return False
    except Exception as e:
        print("[X] Unexpected error: %s" % e)
        return False


def test_local_fallback():
    """Test local fallback responses"""
    print("\n" + "="*60)
    print("Testing Local Fallback Responses...")
    print("="*60)
    
    try:
        from emotion_detector import detect_emotion, get_emotion_emoji
        from chatbot import get_response, get_personalities
        
        # Test emotion detection
        test_text = "I'm feeling happy today!"
        emotion = detect_emotion(test_text)
        print("[OK] Emotion detection works: '%s' -> %s %s" % (test_text, emotion, get_emotion_emoji(emotion)))
        
        # Test local response
        response, emotion = get_response("I'm feeling sad", "empathetic")
        print("[OK] Local response works: %s..." % response[:100])
        
        # Test personalities
        personalities = get_personalities()
        print("[OK] Available personalities: %s" % ", ".join(personalities))
        
        return True
        
    except Exception as e:
        print("[X] Local fallback test failed: %s" % e)
        return False


def main():
    """Run all API tests"""
    print("\n" + "="*60)
    print("Emotional Support AI - API Verification")
    print("="*60)
    
    results = {
        "Google AI": False,
        "Hugging Face": False,
        "Local Fallback": False
    }
    
    # Test local fallback first (always works)
    results["Local Fallback"] = test_local_fallback()
    
    # Test APIs
    results["Google AI"] = test_google_ai()
    results["Hugging Face"] = test_huggingface()
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    all_passed = True
    for service, passed in results.items():
        status = "[OK] PASS" if passed else "[X] FAIL"
        print("%s: %s" % (service, status))
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    
    if results["Local Fallback"]:
        print("[OK] Application will work with local fallback responses")
        if results["Google AI"] or results["Hugging Face"]:
            print("[OK] AI-powered responses also available")
        else:
            print("[!] For AI-powered responses, configure API keys in env/.env")
    else:
        print("[X] Local fallback not working - please check installation")
    
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
