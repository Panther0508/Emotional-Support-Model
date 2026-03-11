# wsgi.py - WSGI entry point for deployment
import os
from app import app

# Application is exposed as 'app' for WSGI servers
# This file is used by gunicorn, uwsgi, and other WSGI servers

if __name__ == "__main__":
    # For local development
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
