from flask import Blueprint, render_template
import logging

bp = Blueprint('home', __name__, url_prefix='/')
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    """Home page route"""
    logger.info('Home page accessed')
    return render_template('index.html')
