"""
Hugging Face Integration Module
Provides functionality for making real API calls to Hugging Face Inference API.
Supports various tasks including text generation, text-to-text, and more.
"""

import requests
from typing import Optional, Dict, Any, List, Union
from apis.api_config import get_config, APIConfig

# Import HuggingFace Hub for InferenceClient
try:
    from huggingface_hub import InferenceClient
    HF_CLIENT_AVAILABLE = True
except ImportError:
    HF_CLIENT_AVAILABLE = False
    InferenceClient = None


class HuggingFaceError(Exception):
    """Custom exception for Hugging Face API errors."""
    pass


class AuthenticationError(HuggingFaceError):
    """Raised when authentication fails."""
    pass


class RateLimitError(HuggingFaceError):
    """Raised when rate limit is exceeded."""
    pass


class ModelError(HuggingFaceError):
    """Raised when there's an error with the model."""
    pass


class APIResponseError(HuggingFaceError):
    """Raised when API returns an error response."""
    pass


class HuggingFaceClient:
    """
    Client for interacting with Hugging Face Inference API.
    Supports various ML tasks with proper error handling.
    """
    
    # Supported tasks and their endpoints
    TASK_ENDPOINTS = {
        "text-generation": "/models",
        "text-to-text-generation": "/models",
        "summarization": "/models",
        "translation": "/models",
        "question-answering": "/models",
        "sentence-similarity": "/pipeline/sentence-similarity",
        "feature-extraction": "/pipeline/feature-extraction",
        "fill-mask": "/pipeline/fill-mask",
        "token-classification": "/pipeline/token-classification",
        "text-classification": "/pipeline/text-classification",
    }
    
    def __init__(self, config: Optional[APIConfig] = None):
        """
        Initialize the Hugging Face client.
        
        Args:
            config: Optional APIConfig instance. Uses global config if not provided.
        """
        self.config = config or get_config()
        self.base_url = self.config.HF_API_BASE_URL
        self._validate_credentials()
    
    def _validate_credentials(self) -> None:
        """Validate that Hugging Face credentials are configured."""
        if not self.config.is_hf_configured:
            raise AuthenticationError(
                "Hugging Face API token not configured. "
                "Please set HF_TOKEN in your .env file."
            )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return self.config.get_hf_headers()
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 60
    ) -> Union[Dict[str, Any], List, str]:
        """
        Make a request to the Hugging Face API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            timeout: Request timeout in seconds
            
        Returns:
            API response (dict, list, or string)
            
        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ModelError: If there's an error with the model
            APIResponseError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "POST":
                response = requests.post(
                    url,
                    headers=self._get_headers(),
                    json=data,
                    params=params,
                    timeout=timeout
                )
            elif method.upper() == "GET":
                response = requests.get(
                    url,
                    headers=self._get_headers(),
                    params=params,
                    timeout=timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Handle specific status codes
            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Please check your HF_TOKEN in .env file."
                )
            elif response.status_code == 403:
                raise AuthenticationError(
                    "Access forbidden. Your token may not have sufficient permissions."
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded. Please wait and try again."
                )
            elif response.status_code == 503:
                raise ModelError(
                    "Model service unavailable. The model may be loading or temporarily unavailable."
                )
            elif response.status_code >= 400:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get("error", error_detail)
                except ValueError:
                    pass
                raise APIResponseError(
                    f"API request failed: {response.status_code} - {error_detail}"
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.Timeout:
            raise HuggingFaceError("Request timed out. Please try again.")
        except requests.ConnectionError:
            raise HuggingFaceError("Connection error. Please check your internet connection.")
    
    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_new_tokens: int = 250,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True,
        return_full_text: bool = False
    ) -> str:
        """
        Generate text using a text generation model.
        
        Args:
            prompt: Input prompt/text
            model: Model name (defaults to meta-llama/Llama-3.2-1B-Instruct)
            max_new_tokens: Maximum tokens to generate
            temperature: Controls randomness (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            do_sample: Whether to use sampling
            return_full_text: Whether to include prompt in output
            
        Returns:
            str: Generated text
            
        Raises:
            HuggingFaceError: For any API-related errors
        """
        # Use the new InferenceClient approach if available
        if HF_CLIENT_AVAILABLE:
            try:
                client = InferenceClient(token=self.config.hf_token)
                # Use chat_completion for better conversational responses
                model = model or "meta-llama/Llama-3.2-1B-Instruct"
                
                # Add system instruction to enforce English responses
                result = client.chat_completion(
                    messages=[
                        {"role": "system", "content": "You are a supportive emotional support assistant. Always respond in English only, regardless of the language used by the user. Keep responses concise and caring."},
                        {"role": "user", "content": prompt}
                    ],
                    model=model,
                    max_tokens=max_new_tokens,
                    temperature=temperature
                )
                
                # Extract the response content
                if hasattr(result, 'choices') and len(result.choices) > 0:
                    return result.choices[0].message.content
                return str(result)
                
            except Exception as e:
                # Fall back to old method if InferenceClient fails
                print(f"InferenceClient error: {e}")
        
        # Fallback to old method
        model = model or self.config.HF_DEFAULT_MODEL
        endpoint = f"/models/{model}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": do_sample,
                "return_full_text": return_full_text
            }
        }
        
        result = self._make_request("POST", endpoint, data=payload)
        
        # Parse the response
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict):
                generated_text = result[0].get("generated_text", "")
                if isinstance(generated_text, list) and len(generated_text) > 0:
                    return generated_text[0].get("generated_text", str(result))
                return generated_text
            return str(result[0])
        elif isinstance(result, dict):
            return result.get("generated_text", str(result))
        
        return str(result)
    
    def text_to_text(
        self,
        text: str,
        model: Optional[str] = None,
        max_new_tokens: int = 250,
        temperature: float = 0.7
    ) -> str:
        """
        Perform text-to-text generation (e.g., translation, summarization).
        
        Args:
            text: Input text
            model: Model name
            max_new_tokens: Maximum tokens to generate
            temperature: Controls randomness
            
        Returns:
            str: Generated text
        """
        model = model or self.config.HF_DEFAULT_MODEL
        endpoint = f"/models/{model}"
        
        payload = {
            "inputs": text,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature
            }
        }
        
        result = self._make_request("POST", endpoint, data=payload)
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", str(result[0]))
        elif isinstance(result, dict):
            return result.get("generated_text", str(result))
        
        return str(result)
    
    def classify_text(
        self,
        text: Union[str, List[str]],
        model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    ) -> List[Dict[str, Any]]:
        """
        Classify text using a text classification model.
        
        Args:
            text: Text or list of texts to classify
            model: Classification model name
            
        Returns:
            List of classification results
        """
        endpoint = f"/models/{model}"
        
        payload = {"inputs": text}
        
        result = self._make_request("POST", endpoint, data=payload)
        return result
    
    def sentiment_analysis(
        self,
        text: Union[str, List[str]],
        model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    ) -> List[Dict[str, Any]]:
        """
        Perform sentiment analysis on text.
        
        Args:
            text: Text or list of texts to analyze
            model: Sentiment analysis model
            
        Returns:
            List of sentiment results with labels and scores
        """
        return self.classify_text(text, model)
    
    def summarize(
        self,
        text: str,
        model: str = "facebook/bart-large-cnn",
        max_length: int = 150,
        min_length: int = 40
    ) -> str:
        """
        Summarize text using a summarization model.
        
        Args:
            text: Text to summarize
            model: Summarization model
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            str: Generated summary
        """
        endpoint = f"/models/{model}"
        
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length
            }
        }
        
        result = self._make_request("POST", endpoint, data=payload)
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("summary_text", str(result[0]))
        
        return str(result)
    
    def translate(
        self,
        text: str,
        model: str = "Helsinki-NLP/opus-mt-en-fr",
        max_length: int = 512
    ) -> str:
        """
        Translate text using a translation model.
        
        Args:
            text: Text to translate
            model: Translation model
            max_length: Maximum output length
            
        Returns:
            str: Translated text
        """
        endpoint = f"/models/{model}"
        
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": max_length
            }
        }
        
        result = self._make_request("POST", endpoint, data=payload)
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("translation_text", str(result[0]))
        
        return str(result)
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model: Model name
            
        Returns:
            dict: Model information
        """
        endpoint = f"/models/{model}"
        return self._make_request("GET", endpoint)
    
    def list_models(
        self,
        task: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        List available models.
        
        Args:
            task: Optional task filter (e.g., "text-generation")
            limit: Number of models to return
            
        Returns:
            List of model info dicts
        """
        params = {"limit": limit}
        if task:
            params["pipeline_tag"] = task
        
        return self._make_request("GET", "/models", params=params)
    
    def test_connection(self, model: Optional[str] = None) -> bool:
        """
        Test the Hugging Face API connection.
        
        Args:
            model: Optional model to test with
            
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            result = self.generate_text(
                prompt="Hello, how are you?",
                model=model or self.config.HF_DEFAULT_MODEL,
                max_new_tokens=20
            )
            return bool(result)
        except HuggingFaceError:
            return False


def get_huggingface_client() -> HuggingFaceClient:
    """
    Get a configured Hugging Face client instance.
    
    Returns:
        HuggingFaceClient: Configured client instance
    """
    return HuggingFaceClient()
