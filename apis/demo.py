"""
API Demo Script
Demonstrates authentication and usage of both Google AI (Gemini) and Hugging Face APIs.
This script shows how to properly use the modular API integrations with error handling.
"""

import sys
from typing import Optional

# Import API modules
from apis.api_config import validate_environment, get_config, APIConfig
from apis.google_ai import GoogleAIClient, GoogleAIError
from apis.huggingface_api import HuggingFaceClient, HuggingFaceError


class APIDemo:
    """
    Demonstrates usage of both Google AI and Hugging Face APIs.
    Provides comprehensive examples with proper error handling.
    """
    
    def __init__(self):
        """Initialize the demo with configuration validation."""
        self.config: Optional[APIConfig] = None
        self.google_client: Optional[GoogleAIClient] = None
        self.hf_client: Optional[HuggingFaceClient] = None
        
    def setup(self) -> bool:
        """
        Set up API clients after validating configuration.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        print("=" * 60)
        print("API Configuration & Demo Setup")
        print("=" * 60)
        
        # Validate environment
        if not validate_environment():
            print("\n❌ Setup failed: Missing API credentials")
            return False
        
        # Initialize clients
        try:
            self.config = get_config()
            
            if self.config.is_google_configured:
                self.google_client = GoogleAIClient(self.config)
                print("\n✅ Google AI Client initialized")
            
            if self.config.is_hf_configured:
                self.hf_client = HuggingFaceClient(self.config)
                print("✅ Hugging Face Client initialized")
            
            print("\n✅ Setup complete!")
            return True
            
        except Exception as e:
            print(f"\n❌ Setup failed: {str(e)}")
            return False
    
    def demo_google_ai(self) -> None:
        """Demonstrate Google AI (Gemini) API usage."""
        if not self.google_client:
            print("\n⚠️  Google AI client not available (not configured)")
            return
            
        print("\n" + "=" * 60)
        print("Google AI (Gemini) API Demo")
        print("=" * 60)
        
        # Test 1: Simple text generation
        print("\n[1] Simple Text Generation:")
        print("-" * 40)
        try:
            response = self.google_client.generate_text(
                prompt="Write a short poem about artificial intelligence.",
                temperature=0.8,
                max_output_tokens=150
            )
            print(f"Response: {response[:200]}..." if len(response) > 200 else f"Response: {response}")
            print("✅ Text generation successful")
        except GoogleAIError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 2: Text generation with system instruction
        print("\n[2] Text Generation with System Instruction:")
        print("-" * 40)
        try:
            response = self.google_client.generate_text(
                prompt="Explain quantum computing to a 5-year-old.",
                system_instruction="You are a helpful assistant that explains complex topics simply.",
                temperature=0.7,
                max_output_tokens=200
            )
            print(f"Response: {response[:300]}..." if len(response) > 300 else f"Response: {response}")
            print("✅ System instruction test successful")
        except GoogleAIError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 3: Chat-style conversation
        print("\n[3] Chat-Style Conversation:")
        print("-" * 40)
        try:
            messages = [
                {"role": "user", "content": "What is the capital of France?"},
                {"role": "assistant", "content": "The capital of France is Paris."},
                {"role": "user", "content": "What is its population?"}
            ]
            response = self.google_client.chat(
                messages=messages,
                temperature=0.7
            )
            print(f"Response: {response}")
            print("✅ Chat test successful")
        except GoogleAIError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 4: Test connection
        print("\n[4] Connection Test:")
        print("-" * 40)
        try:
            is_connected = self.google_client.test_connection()
            if is_connected:
                print("✅ Google AI API connection successful")
            else:
                print("❌ Google AI API connection failed")
        except GoogleAIError as e:
            print(f"❌ Connection test error: {str(e)}")
    
    def demo_huggingface(self) -> None:
        """Demonstrate Hugging Face API usage."""
        if not self.hf_client:
            print("\n⚠️  Hugging Face client not available (not configured)")
            return
            
        print("\n" + "=" * 60)
        print("Hugging Face API Demo")
        print("=" * 60)
        
        # Test 1: Text Generation
        print("\n[1] Text Generation (FLAN-T5):")
        print("-" * 40)
        try:
            response = self.hf_client.generate_text(
                prompt="Write a short story about a robot:",
                model="google/flan-t5-base",
                max_new_tokens=100,
                temperature=0.8
            )
            print(f"Response: {response[:200]}..." if len(response) > 200 else f"Response: {response}")
            print("✅ Text generation successful")
        except HuggingFaceError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 2: Sentiment Analysis
        print("\n[2] Sentiment Analysis:")
        print("-" * 40)
        try:
            result = self.hf_client.sentiment_analysis(
                text="I absolutely love this product! It's amazing!",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            print(f"Input: 'I absolutely love this product! It's amazing!'")
            print(f"Result: {result}")
            print("✅ Sentiment analysis successful")
        except HuggingFaceError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 3: Summarization
        print("\n[3] Text Summarization (BART):")
        print("-" * 40)
        try:
            text = """Artificial intelligence (AI) is intelligence demonstrated by machines, 
            as opposed to the natural intelligence displayed by humans or animals. 
            Leading AI textbooks define the field as the study of "intelligent agents": 
            any device that perceives its environment and takes actions that maximize 
            its chance of successfully achieving its goals. Some popular uses of AI 
            include computer vision, natural language processing (NLP), and recommendation systems."""
            
            summary = self.hf_client.summarize(
                text=text,
                model="facebook/bart-large-cnn",
                max_length=100,
                min_length=30
            )
            print(f"Input: {text[:100]}...")
            print(f"Summary: {summary}")
            print("✅ Summarization successful")
        except HuggingFaceError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 4: Text Classification
        print("\n[4] Text Classification:")
        print("-" * 40)
        try:
            result = self.hf_client.classify_text(
                text="This movie was terrible. I hated every minute of it.",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            print(f"Input: 'This movie was terrible. I hated every minute of it.'")
            print(f"Result: {result}")
            print("✅ Classification successful")
        except HuggingFaceError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 5: Translation
        print("\n[5] Translation (English to French):")
        print("-" * 40)
        try:
            translation = self.hf_client.translate(
                text="Hello, how are you today?",
                model="Helsinki-NLP/opus-mt-en-fr"
            )
            print(f"Input: 'Hello, how are you today?'")
            print(f"Translation: {translation}")
            print("✅ Translation successful")
        except HuggingFaceError as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 6: Test connection
        print("\n[6] Connection Test:")
        print("-" * 40)
        try:
            is_connected = self.hf_client.test_connection()
            if is_connected:
                print("✅ Hugging Face API connection successful")
            else:
                print("❌ Hugging Face API connection failed")
        except HuggingFaceError as e:
            print(f"❌ Connection test error: {str(e)}")
    
    def demo_combined(self) -> None:
        """Demonstrate using both APIs together."""
        if not self.google_client or not self.hf_client:
            print("\n⚠️  Combined demo skipped: Both clients required")
            return
            
        print("\n" + "=" * 60)
        print("Combined API Demo")
        print("=" * 60)
        
        print("\n[1] Emotion Detection Pipeline:")
        print("-" * 40)
        try:
            # Step 1: Analyze sentiment with Hugging Face
            sentiment_result = self.hf_client.sentiment_analysis(
                text="I'm feeling really anxious about this presentation tomorrow."
            )
            print(f"User input: \"I'm feeling really anxious about this presentation tomorrow.\"")
            print(f"Hugging Face Sentiment: {sentiment_result}")
            
            # Step 2: Generate supportive response with Google AI
            response = self.google_client.generate_text(
                prompt="""The user expressed anxiety about a presentation. 
                Provide a supportive, calming response with practical tips.""",
                system_instruction="You are a supportive emotional support assistant.",
                temperature=0.7,
                max_output_tokens=200
            )
            print(f"\nGoogle AI Supportive Response: {response}")
            print("✅ Combined pipeline successful")
            
        except (HuggingFaceError, GoogleAIError) as e:
            print(f"❌ Error: {str(e)}")
    
    def run_all_demos(self) -> None:
        """Run all API demos."""
        # Setup
        if not self.setup():
            sys.exit(1)
        
        # Run demos
        self.demo_google_ai()
        self.demo_huggingface()
        self.demo_combined()
        
        # Summary
        print("\n" + "=" * 60)
        print("Demo Complete!")
        print("=" * 60)
        print("\n📝 Usage Examples:")
        print("""
# Using Google AI:
from apis.google_ai import GoogleAIClient
client = GoogleAIClient()
response = client.generate_text("Your prompt here")

# Using Hugging Face:
from apis.huggingface_api import HuggingFaceClient
client = HuggingFaceClient()
result = client.generate_text("Your prompt here")
result = client.sentiment_analysis("Your text here")
""")


def main():
    """Main entry point for the demo."""
    demo = APIDemo()
    demo.run_all_demos()


if __name__ == "__main__":
    main()
