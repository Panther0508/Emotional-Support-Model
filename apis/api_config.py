"""
API Configuration Module
Handles environment variables and configuration management for Google AI and Hugging Face APIs.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class APIConfig:
    """
    Central configuration class for managing API credentials and settings.
    Loads environment variables from .env file and provides secure access to API keys.
    """
    
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    ENV_PATH: Path = BASE_DIR / "env" / ".env"
    
    # Hugging Face API settings
    HF_API_BASE_URL: str = "https://router.huggingface.co"
    HF_DEFAULT_MODEL: str = "google/flan-t5-base"
    
    # Google AI (Gemini) API settings
    GOOGLE_API_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    GOOGLE_DEFAULT_MODEL: str = "gemini-2.0-flash"
    
    def __init__(self, env_path: Optional[Path] = None):
        """
        Initialize configuration and load environment variables.
        
        Args:
            env_path: Optional custom path to .env file
        """
        self.env_path = env_path or self.ENV_PATH
        self._load_environment()
    
    def _load_environment(self) -> None:
        """Load environment variables from .env file."""
        # Try multiple locations for the .env file
        env_paths = [
            self.env_path,
            self.BASE_DIR / ".env",
            Path("env/.env"),
            Path(".env")
        ]
        
        for path in env_paths:
            if path.exists():
                load_dotenv(dotenv_path=path)
                print(f"Loaded environment from: {path}")
                return
        
        print(f"Warning: .env file not found. Searched in: {env_paths}")
    
    @property
    def hf_token(self) -> Optional[str]:
        """Get Hugging Face API token from environment variables."""
        token = os.getenv("HF_TOKEN")
        if not token or token == "your_huggingface_token_here":
            return None
        return token.strip()
    
    @property
    def google_token(self) -> Optional[str]:
        """Get Google AI API key from environment variables."""
        token = os.getenv("GOOGLE_TOKEN")
        if not token or token == "your_google_ai_key_here":
            return None
        return token.strip()
    
    @property
    def is_hf_configured(self) -> bool:
        """Check if Hugging Face API is properly configured."""
        return self.hf_token is not None
    
    @property
    def is_google_configured(self) -> bool:
        """Check if Google AI API is properly configured."""
        return self.google_token is not None
    
    @property
    def is_fully_configured(self) -> bool:
        """Check if both APIs are properly configured."""
        return self.is_hf_configured and self.is_google_configured
    
    def get_hf_headers(self) -> dict:
        """
        Get headers for Hugging Face API requests.
        
        Returns:
            dict: Headers including Authorization header with Bearer token
        """
        if not self.is_hf_configured:
            raise ValueError("Hugging Face API token not configured. Set HF_TOKEN in .env file.")
        
        return {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
    
    def validate_configuration(self) -> dict:
        """
        Validate the current configuration and return status.
        
        Returns:
            dict: Configuration status for each API
        """
        return {
            "huggingface": {
                "configured": self.is_hf_configured,
                "token_present": bool(os.getenv("HF_TOKEN")),
                "token_valid": self.is_hf_configured
            },
            "google_ai": {
                "configured": self.is_google_configured,
                "token_present": bool(os.getenv("GOOGLE_TOKEN")),
                "token_valid": self.is_google_configured
            },
            "fully_configured": self.is_fully_configured
        }


# Global configuration instance
config = APIConfig()


def get_config() -> APIConfig:
    """Get the global configuration instance."""
    return config


def validate_environment() -> bool:
    """
    Validate that the environment is properly set up.
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    config = get_config()
    status = config.validate_configuration()
    
    if not status["fully_configured"]:
        print("\n⚠️  API Configuration Incomplete:")
        if not status["huggingface"]["configured"]:
            print("  - Hugging Face: Missing or invalid HF_TOKEN")
        if not status["google_ai"]["configured"]:
            print("  - Google AI: Missing or invalid GOOGLE_TOKEN")
        print("\nPlease copy env/.env.example to env/.env and add your API keys.")
        return False
    
    print("\n✅ API Configuration Complete:")
    print("  - Hugging Face: ✅ Configured")
    print("  - Google AI: ✅ Configured")
    return True
