import os
from flask import Flask, render_template, send_from_directory, request
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()
    
    # Create Flask app instance
    app = Flask(__name__, instance_relative_config=True)
    
    # Clear log files at startup
    log_dir = Path(app.root_path).parent / 'logs'
    if log_dir.exists():
        for log_file in log_dir.glob('*.log'):
            try:
                log_file.write_text('')  # Clear the file contents
            except Exception as e:
                print(f"Error clearing log file {log_file}: {e}")
    
    # Determine environment
    env = os.getenv('FLASK_ENV', 'development')
    debug_mode = env == 'development'
    
    # Configure app based on environment
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
            DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
            FLASK_ENV=env,
            LOG_DIR=str(log_dir),
            LOG_LEVEL='DEBUG' if debug_mode else 'INFO',
            LOG_MAX_BYTES=10 * 1024 * 1024,  # 10MB
            LOG_BACKUP_COUNT=3,
            LOG_FILE_CONFIGS={
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
        )
    else:
        app.config.update(test_config)
        
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import and setup logger
    from .utils.logger import setup_logger
    setup_logger(app)
    
    # Log initial configuration
    app.logger.info(f"Current environment: {env}")
    app.logger.info(f"Debug mode: {debug_mode}")
    app.logger.info(f"Log level: {app.config['LOG_LEVEL']}")
    
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
        app.logger.error(f'Page not found: {request.url}')
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
