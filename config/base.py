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
    """Base configuration class for the Flask application.
    
    This class provides default values and loads configuration from environment variables.
    Environment-specific configurations (development/production) inherit from this class.
    """
    # Basic Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change-in-production')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # Environment configuration
    FLASK_ENV = 'production'  # Default to production for safety
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    
    # Logging configuration
    LOG_TYPE = os.getenv('LOG_TYPE', 'file')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'simple')
    LOG_DIR = Path(__file__).parent.parent / os.getenv('LOG_DIR', 'logs')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # Default: 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 10))

    @classmethod
    def load_environment(cls):
        """Load environment variables from appropriate .env files"""
        basedir = Path(__file__).parent.parent
        
        # Try to load main .env first
        main_env = basedir / '.env'
        if main_env.exists():
            load_dotenv(main_env)
            logger.debug(f"Loaded main environment from {main_env}")
        
        # Get environment and load specific config
        flask_env = os.getenv('FLASK_ENV', 'production')
        env_file = basedir / f'.env.{flask_env}'
        
        if env_file.exists():
            load_dotenv(env_file, override=True)
            logger.debug(f"Loaded {flask_env} environment from {env_file}")
            
            # Set FLASK_ENV in the class after loading environment
            cls.FLASK_ENV = flask_env
            
        elif flask_env == 'production':
            # In production (like on Render), we expect env vars to be set in the platform
            logger.debug("Running in production mode with platform environment variables")
            cls.FLASK_ENV = 'production'
            
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

    @classmethod
    def get_config(cls):
        """Get the appropriate configuration class based on FLASK_ENV"""
        # Load environment variables first
        cls.load_environment()
        
        # Import here to avoid circular imports
        from .dev import DevelopmentConfig
        from .prod import ProductionConfig
        
        configs = {
            'development': DevelopmentConfig,
            'production': ProductionConfig
        }
        
        # Get environment, defaulting to production for safety
        flask_env = cls.FLASK_ENV
        
        # Return appropriate config class
        return configs.get(flask_env, ProductionConfig)

    def __init__(self):
        """Create required directories on instantiation"""
        self.LOG_DIR.mkdir(exist_ok=True)

# Load environment at module level
load_environment()
