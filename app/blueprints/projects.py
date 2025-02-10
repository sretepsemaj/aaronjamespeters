from flask import Blueprint, jsonify, render_template
import logging

bp = Blueprint('projects', __name__, url_prefix='/projects')
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    """Projects page route"""
    logger.info('Projects page accessed')
    return render_template('projects/index.html', title='Projects')

@bp.route('/api/data')
def get_projects():
    """API endpoint to get projects data"""
    logger.info('Accessing projects API endpoint')
    try:
        projects = [
            {
                'title': 'Portfolio Website',
                'description': 'A Flask-based portfolio website showcasing my work and experience',
                'technologies': [
                    'Python/Flask',
                    'Bootstrap 5',
                    'Responsive Design'
                ]
            }
            # Add more projects here
        ]
        return jsonify(projects)
    except Exception as e:
        logger.error(f'Error retrieving project data: {str(e)}')
        return jsonify({'error': 'Failed to retrieve project data'}), 500
