from flask import Blueprint, jsonify, render_template
import logging
from pathlib import Path

bp = Blueprint('bio', __name__, url_prefix='/bio')
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    """Bio page route"""
    logger.info('Bio page accessed')
    try:
        bio_path = Path(__file__).parent.parent / 'media' / 'txt' / 'aaronjamespetersBIO.txt'
        with open(bio_path, 'r') as file:
            bio_text = file.read()
        
        # Split the content into paragraphs
        paragraphs = [p.strip() for p in bio_text.split('\n\n') if p.strip()]
        
        return render_template('bio/index.html', title='Bio', paragraphs=paragraphs)
    except Exception as e:
        logger.error(f'Error reading bio file: {str(e)}')
        return render_template('bio/index.html', title='Bio', paragraphs=[])

@bp.route('/api/data')
def get_bio_data():
    """API endpoint to get bio information"""
    logger.info('Accessing bio data API endpoint')
    try:
        bio_path = Path(__file__).parent.parent / 'media' / 'txt' / 'aaronjamespetersBIO.txt'
        with open(bio_path, 'r') as file:
            bio_text = file.read()
        
        paragraphs = [p.strip() for p in bio_text.split('\n\n') if p.strip()]
        
        bio_data = {
            'title': paragraphs[0] if paragraphs else '',
            'content': paragraphs[1:] if len(paragraphs) > 1 else []
        }
        return jsonify(bio_data)
    except Exception as e:
        logger.error(f'Error retrieving bio data: {str(e)}')
        return jsonify({'error': 'Failed to retrieve bio data'}), 500
