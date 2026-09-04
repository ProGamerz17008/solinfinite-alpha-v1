import os
import sys

# Ensure root folder is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

# Export app instance for Vercel Serverless Function
handler = app
