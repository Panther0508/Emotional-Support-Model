# Procfile - Alternative deployment configuration for Render
web: gunicorn wsgi:app --timeout 120 --workers 2 --bind 0.0.0.0:$PORT
