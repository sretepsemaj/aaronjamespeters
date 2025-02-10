import os
from flask import Flask, render_template, send_from_directory
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from datetime import datetime

def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()
    
    # Create Flask app instance
    app = Flask(__name__, instance_relative_config=True)
    
    # Determine environment
    env = os.getenv('FLASK_ENV', 'development')
    debug_mode = env == 'development'
    
    # Configure app based on environment
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
            DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        )
    else:
        app.config.update(test_config)
        
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # Configure logging
    log_level = logging.DEBUG if debug_mode else logging.INFO
    log_format = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Configure file handlers for different log levels
    log_dir = os.path.join(os.path.dirname(app.root_path), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    file_handlers = {
        'debug': RotatingFileHandler(os.path.join(log_dir, 'debug.log'), maxBytes=10485760, backupCount=5),
        'info': RotatingFileHandler(os.path.join(log_dir, 'info.log'), maxBytes=10485760, backupCount=5),
        'error': RotatingFileHandler(os.path.join(log_dir, 'error.log'), maxBytes=10485760, backupCount=5)
    }
    
    for handler in file_handlers.values():
        handler.setFormatter(formatter)
    
    file_handlers['debug'].setLevel(logging.DEBUG)
    file_handlers['info'].setLevel(logging.INFO)
    file_handlers['error'].setLevel(logging.ERROR)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove any existing handlers to avoid duplicates
    root_logger.handlers = []
    
    # Add all handlers
    root_logger.addHandler(console_handler)
    for handler in file_handlers.values():
        root_logger.addHandler(handler)
    
    # Log startup information
    app.logger.info('Current environment: %s', env)
    app.logger.info('Debug mode: %s', debug_mode)
    app.logger.info('Log level: %s', logging.getLevelName(log_level))
    app.logger.info('Log format: %s', log_format)
    
    # Context processor for templates
    @app.context_processor
    def utility_processor():
        return {'now': datetime.now()}

    # Main route
    @app.route('/')
    def index():
        app.logger.info('Home page accessed')
        return render_template('index.html', title='Home')

    # Media files endpoint
    @app.route('/media/<path:filename>')
    def media(filename):
        media_dir = os.path.join(app.root_path, 'media')
        return send_from_directory(media_dir, filename)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'Page not found: {error}')
        return {'error': 'Page not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return {'error': 'Internal server error'}, 500

    # Register blueprints
    from .blueprints import home, bio, projects, resume, youtube
    app.register_blueprint(home.bp)
    app.register_blueprint(bio.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(resume.bp)
    app.register_blueprint(youtube.bp)
    
    return app
