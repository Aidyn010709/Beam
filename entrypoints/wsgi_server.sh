#!/bin/sh
echo "Migrate"
python manage.py migrate
echo "Run server"
gunicorn --workers=5 --threads=2 --worker-class=gthread -b 0.0.0.0:8000 beam.wsgi --reload --log-level=info
