import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import app

try:
    import serverless_wsgi
    def handler(event, context):
        return serverless_wsgi.handle_request(app, event, context)
except ImportError:
    handler = app
