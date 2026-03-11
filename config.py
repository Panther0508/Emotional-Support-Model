# config.py - Centralized Configuration for Emotional Support AI
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # Directories
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    USERS_DIR = os.path.join(BASE_DIR, 'users')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Files
    STATISTICS_FILE = os.path.join(DATA_DIR, 'statistics.json')
    COPING_SUGGESTIONS_FILE = os.path.join(BASE_DIR, 'coping_suggestions.json')
    TRAINING_DATA_FILE = os.path.join(BASE_DIR, 'training_data.json')
    
    # Chat settings
    MAX_HISTORY_MESSAGES = 100
    
    # Emotion detection settings
    SENTIMENT_THRESHOLD = 0.3
    
    # Available personalities
    PERSONALITIES = ['empathetic', 'funny', 'motivational', 'calm']
    DEFAULT_PERSONALITY = 'empathetic'
    
    # Allowed emotions
    EMOTIONS = ['happy', 'sad', 'anxious', 'angry', 'neutral']
    
    # Create directories on init
    @staticmethod
    def init_app(app):
        """Initialize application"""
        os.makedirs(Config.USERS_DIR, exist_ok=True)
        os.makedirs(Config.DATA_DIR, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
