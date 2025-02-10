from .base import Config

class DevelopmentConfig(Config):
    DEBUG = True
    
    # Development-specific logging settings
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s'
    
    # Detailed logging configuration
    LOG_FILE_CONFIGS = {
        'debug': {
            'filename': 'debug.log',
            'level': 'DEBUG',
            'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s'
        },
        'info': {
            'filename': 'info.log',
            'level': 'INFO',
            'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s'
        },
        'error': {
            'filename': 'error.log',
            'level': 'ERROR',
            'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s'
        }
    }
    
    def __init__(self):
        print("Loading DevelopmentConfig")
