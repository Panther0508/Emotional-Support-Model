"""
Google AI (Gemini) Integration Module
Provides functionality for making real API calls to Google Gemini models.
"""

import requests
from typing import Optional, Dict, Any, List
from apis.api_config import get_config, APIConfig


class GoogleAIError(Exception):
    """Custom exception for Google AI API errors."""
    pass


class AuthenticationError(GoogleAIError):
    """Raised when authentication fails."""
    pass


class RateLimitError(GoogleAIError):
    """Raised when rate limit is exceeded."""
    pass


class APIResponseError(GoogleAIError):
    """Raised when API returns an error response."""
    pass


class GoogleAIClient:
    """
    Client for interacting with Google Gemini API.
    Supports text generation with proper error handling and retry logic.
    """
    
    def __init__(self, config: Optional[APIConfig] = None):
        """
        Initialize the Google AI client.
        
        Args:
            config: Optional APIConfig instance. Uses global config if not provided.
        """
        self.config = config or get_config()
        self._validate_credentials()
    
    def _validate_credentials(self) -> None:
        """Validate that Google AI credentials are configured."""
        if not self.config.is_google_configured:
            raise AuthenticationError(
                "Google AI API key not configured. "
                "Please set GOOGLE_TOKEN in your .env file."
            )
    
    def _get_api_url(self, model: str) -> str:
        """Get the full API URL for the given model."""
        return f"{self.config.GOOGLE_API_BASE_URL}/models/{model}:generateContent"
    
    def _make_request(
        self, 
        url: str, 
        headers: Dict[str, str], 
        payload: Dict[str, Any],
        timeout: int = 60
    ) -> Dict[str, Any]:
        """
        Make a POST request to the Google AI API.
        
        Args:
            url: Full API URL
            headers: Request headers including API key
            payload: Request body
            timeout: Request timeout in seconds
            
        Returns:
            dict: API response JSON
            
        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIResponseError: For other API errors
            requests.RequestException: For network errors
        """
        try:
            response = requests.post(
                url, 
                headers=headers, 
                json=payload, 
                timeout=timeout
            )
            
            # Handle specific HTTP status codes
            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Please check your GOOGLE_TOKEN in .env file."
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded. Please wait and try again."
                )
            elif response.status_code >= 400:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get("error", {}).get("message", error_detail)
                except ValueError:
                    pass
                raise APIResponseError(
                    f"API request failed with status {response.status_code}: {error_detail}"
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.Timeout:
            raise GoogleAIError("Request timed out. Please try again.")
        except requests.ConnectionError:
            raise GoogleAIError("Connection error. Please check your internet connection.")
    
    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 2048,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate text using Google Gemini model.
        
        Args:
            prompt: The input prompt/text
            model: Model name (defaults to gemini-2.0-flash)
            temperature: Controls randomness (0.0 to 1.0)
            max_output_tokens: Maximum tokens in output
            system_instruction: Optional system instruction
            
        Returns:
            str: Generated text response
            
        Raises:
            GoogleAIError: For any API-related errors
        """
        model = model or self.config.GOOGLE_DEFAULT_MODEL
        api_url = self._get_api_url(model)
        
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json"
        }
        
        # Build the request payload
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        
        generation_config = {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
            "topP": 0.95,
            "topK": 40
        }
        
        payload = {
            "contents": contents,
            "generationConfig": generation_config
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        
        # Make the API request with API key as query parameter
        params = {"key": self.config.google_token}
        
        try:
            response = requests.post(
                api_url,
                headers=headers,
                params=params,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Please check your GOOGLE_TOKEN in .env file."
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded. Please wait and try again."
                )
            elif response.status_code >= 400:
                raise APIResponseError(
                    f"API request failed: {response.status_code} - {response.text}"
                )
            
            result = response.json()
            
            # Extract the generated text from the response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        return parts[0]["text"]
            
            return str(result)
            
        except requests.RequestException as e:
            raise GoogleAIError(f"Request failed: {str(e)}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate a response using chat-style message history.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            model: Model name (defaults to gemini-2.0-flash)
            temperature: Controls randomness
            system_instruction: Optional system instruction
            
        Returns:
            str: Generated response
        """
        # Convert messages to contents format
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            # Map 'assistant' to 'model' for Gemini
            if role == "assistant":
                role = "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}]
            })
        
        model = model or self.config.GOOGLE_DEFAULT_MODEL
        api_url = self._get_api_url(model)
        
        generation_config = {
            "temperature": temperature,
            "maxOutputTokens": 2048,
            "topP": 0.95,
            "topK": 40
        }
        
        payload = {
            "contents": contents,
            "generationConfig": generation_config
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        
        headers = {"Content-Type": "application/json"}
        params = {"key": self.config.google_token}
        
        response = requests.post(
            api_url,
            headers=headers,
            params=params,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed. Please check your GOOGLE_TOKEN in .env file."
            )
        elif response.status_code >= 400:
            raise APIResponseError(
                f"API request failed: {response.status_code} - {response.text}"
            )
        
        result = response.json()
        
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                if len(parts) > 0 and "text" in parts[0]:
                    return parts[0]["text"]
        
        return str(result)
    
    def test_connection(self) -> bool:
        """
        Test the Google AI API connection.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            response = self.generate_text(
                prompt="Hello",
                max_output_tokens=10
            )
            return bool(response)
        except GoogleAIError:
            return False


def get_google_ai_client() -> GoogleAIClient:
    """
    Get a configured Google AI client instance.
    
    Returns:
        GoogleAIClient: Configured client instance
    """
    return GoogleAIClient()
