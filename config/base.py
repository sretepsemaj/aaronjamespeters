"""Base configuration for the application."""
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def load_environment():
    """Load environment variables from appropriate .env files"""
    basedir = Path(__file__).parent.parent
    
    # Try to load main .env first
    main_env = basedir / '.env'
    if main_env.exists():
        load_dotenv(main_env)
        logger.debug(f"Loaded main environment from {main_env}")
    
    # Default to production if FLASK_ENV is missing (security best practice)
    flask_env = os.getenv('FLASK_ENV', 'production')
    env_file = basedir / f'.env.{flask_env}'
    
    if env_file.exists():
        load_dotenv(env_file, override=True)
        logger.debug(f"Loaded {flask_env} environment from {env_file}")
    elif flask_env == 'production':
        # In production (like on Render), we expect env vars to be set in the platform
        logger.debug("Running in production mode with platform environment variables")
        
        # Validate critical production settings
        if not os.getenv('SECRET_KEY'):
            raise ValueError(
                "Production environment requires SECRET_KEY to be set. "
                "If running on Render, set this in the environment variables section."
            )
    else:
        # If we're not in production and the env file is missing, that's an error
        raise ValueError(
            f"Environment file {env_file} not found. "
            f"Make sure .env.{flask_env} exists for {flask_env} environment"
        )

class Config:
    """Base configuration."""
    
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change-in-production')
    FLASK_APP = os.environ.get('FLASK_APP', 'app.py')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    
    # Application directories
    BASE_DIR = Path(__file__).parent.parent
    INSTANCE_DIR = BASE_DIR / 'instance'
    MEDIA_DIR = BASE_DIR / 'app' / 'media'
    LOG_DIR = BASE_DIR / os.environ.get('LOG_DIR', 'logs')
    
    # Ensure directories exist
    INSTANCE_DIR.mkdir(exist_ok=True)
    MEDIA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    
    # Logging configuration
    LOG_TYPE = os.environ.get('LOG_TYPE', 'stream')  # 'stream' or 'file'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.environ.get('LOG_FORMAT', 'detailed')  # 'simple' or 'detailed'
    LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES', 10485760))  # Default: 10MB
    LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 10))
    
    # Media configuration
    MEDIA_ROOT = str(MEDIA_DIR)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Security settings
    SESSION_COOKIE_SECURE = os.environ.get('FORCE_HTTPS', '0') == '1'
    REMEMBER_COOKIE_SECURE = os.environ.get('FORCE_HTTPS', '0') == '1'
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Security headers
    if os.environ.get('SECURE_HEADERS', '0') == '1':
        TALISMAN_ENABLED = True
        TALISMAN_FORCE_HTTPS = os.environ.get('FORCE_HTTPS', '0') == '1'
        TALISMAN_STRICT_TRANSPORT_SECURITY = True
        TALISMAN_SESSION_COOKIE_SECURE = True
        TALISMAN_CONTENT_SECURITY_POLICY = {
            'default-src': ["'self'"],
            'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", 
                          'https://code.jquery.com',
                          'https://cdn.jsdelivr.net',
                          'https://cdnjs.cloudflare.com'],
            'style-src': ["'self'", "'unsafe-inline'",
                         'https://cdn.jsdelivr.net',
                         'https://cdnjs.cloudflare.com',
                         'https://fonts.googleapis.com'],
            'font-src': ["'self'",
                        'https://cdn.jsdelivr.net',
                        'https://fonts.gstatic.com'],
            'img-src': ["'self'", 'data:', 'https:'],
            'connect-src': ["'self'"]
        }

    @classmethod
    def get_config(cls):
        """Get the appropriate configuration class based on FLASK_ENV"""
        # Load environment variables first
        load_environment()
        
        # Import here to avoid circular imports
        from .dev import DevelopmentConfig
        from .prod import ProductionConfig
        
        configs = {
            'development': DevelopmentConfig,
            'production': ProductionConfig
        }
        
        # Get environment, defaulting to production for safety
        flask_env = os.getenv('FLASK_ENV', 'production').lower().strip()
        logger.debug(f"FLASK_ENV value: '{flask_env}'")
        
        # Return appropriate config class
        return configs.get(flask_env, ProductionConfig)
