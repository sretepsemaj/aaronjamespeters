# Clean any existing Flask environment variables
import os
if 'FLASK_ENV' in os.environ:
    del os.environ['FLASK_ENV']
if 'FLASK_DEBUG' in os.environ:
    del os.environ['FLASK_DEBUG']

from app import create_app
from config.base import load_environment

# Load environment configuration
load_environment()

app = create_app()

if __name__ == '__main__':
    app.run()
