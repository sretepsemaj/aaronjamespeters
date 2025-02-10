from .base import Config

class ProductionConfig(Config):
    DEBUG = False
    
    # Production-specific logging settings
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    
    # Streamlined logging configuration for production
    LOG_FILE_CONFIGS = {
        'info': {
            'filename': 'info.log',
            'level': 'INFO',
            'format': '%(asctime)s %(levelname)s: %(message)s'
        },
        'error': {
            'filename': 'error.log',
            'level': 'ERROR',
            'format': '%(asctime)s %(levelname)s: %(message)s'
        }
    }
    
    def __init__(self):
        super().__init__()
        # Ensure critical settings are present
        if not self.SECRET_KEY or self.SECRET_KEY == 'dev-secret-key-please-change-in-production':
            raise ValueError(
                "Production configuration requires a secure SECRET_KEY. "
                "Please set this in your production environment variables."
            )
