import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

class SSLFilterHandler(RotatingFileHandler):
    """Custom handler that filters out SSL-related errors"""
    def __init__(self, *args, is_development=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_development = is_development
        
    def emit(self, record):
        # Skip SSL-related errors in development
        if self.is_development and hasattr(record, 'msg'):
            msg = str(record.msg).lower()
            if any(x in msg for x in ['ssl', 'https', 'bad request', '\x16\x03\x01']):
                return
        super().emit(record)

def setup_logger(app):
    """Set up the Flask application logger with file handlers."""
    # Create logs directory if it doesn't exist
    log_dir = Path(app.config['LOG_DIR'])
    log_dir.mkdir(exist_ok=True)
    
    # Remove any existing handlers to prevent duplicates
    if app.logger.handlers:
        app.logger.handlers.clear()
    
    # Get the log configurations based on environment
    log_configs = app.config.get('LOG_FILE_CONFIGS', {})
    
    # Check if we're in development environment
    is_development = app.config['FLASK_ENV'] == 'development'
    
    # Set up handlers for each log file
    for log_type, config in log_configs.items():
        log_file = log_dir / config['filename']
        
        # Always use SSLFilterHandler, but only filter in development
        handler = SSLFilterHandler(
            filename=log_file,
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=app.config['LOG_BACKUP_COUNT'],
            is_development=is_development
        )
        
        # Set level for this handler
        level = getattr(logging, config['level'].upper())
        handler.setLevel(level)
        
        # Set formatter
        formatter = logging.Formatter(config['format'])
        handler.setFormatter(formatter)
        
        # Add handler to app logger
        app.logger.addHandler(handler)
    
    # Set the base logging level from config
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL'].upper()))
