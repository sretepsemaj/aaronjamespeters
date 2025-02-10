from flask import Blueprint, render_template, jsonify
import logging
from pathlib import Path

bp = Blueprint('resume', __name__, url_prefix='/resume')
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    """Resume page route"""
    logger.info('Resume page accessed')
    return render_template('resume/index.html')

@bp.route('/api/data')
def get_resume_data():
    """API endpoint to get resume information"""
    try:
        resume_path = Path(__file__).parent.parent / 'media' / 'txt' / 'aaronjamespetersRESUME.txt'
        with open(resume_path, 'r') as file:
            resume_text = file.read()
        
        sections = resume_text.split('\n\n')
        resume_data = {
            'header': sections[0].strip(),
            'contact': sections[1].strip(),
            'sections': []
        }
        
        current_section = None
        current_content = []
        
        for section in sections[2:]:
            lines = section.strip().split('\n')
            # Check if this section starts with an all-caps header (excluding GPA)
            is_header = any(line.isupper() and line.strip() and 'GPA' not in line for line in lines)
            if is_header:
                # If we have a previous section, add it to our data
                if current_section:
                    resume_data['sections'].append({
                        'title': current_section,
                        'content': current_content
                    })
                # Start a new section
                current_section = next(line for line in lines if line.isupper() and line.strip() and 'GPA' not in line)
                current_content = [line for line in lines if line != current_section]
            else:
                current_content.extend(lines)
        
        # Add the last section
        if current_section:
            resume_data['sections'].append({
                'title': current_section,
                'content': current_content
            })
        
        return jsonify(resume_data)
    except Exception as e:
        logger.error(f'Error retrieving resume data: {str(e)}')
        return jsonify({'error': 'Failed to retrieve resume data'}), 500
