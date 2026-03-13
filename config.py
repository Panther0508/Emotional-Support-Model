# config.py - Centralized Configuration for Emotional Support AI
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # Environment
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Directories
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    USERS_DIR = os.path.join(BASE_DIR, 'users')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Database - Support both SQLite (dev) and PostgreSQL (prod)
    # Use DATABASE_URL from environment (provided by Render for PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Use PostgreSQL in production
        if database_url.startswith('postgres://'):
            # Convert postgres:// to postgresql:// for SQLAlchemy
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Use SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATA_DIR, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
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
    
    # NLTK data path
    NLTK_DATA_PATH = os.environ.get('NLTK_DATA', os.path.join(BASE_DIR, 'nltk_data'))
    
    # Create directories on init
    @staticmethod
    def init_app(app):
        """Initialize application"""
        os.makedirs(Config.USERS_DIR, exist_ok=True)
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        
        # Initialize NLTK data path
        import nltk
        nltk.data.path.append(Config.NLTK_DATA_PATH)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # More secure session settings for production
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
