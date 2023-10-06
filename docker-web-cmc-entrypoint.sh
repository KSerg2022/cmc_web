#!/bin/bash

# https://stackoverflow.com/questions/52942913/docker-compose-docker-entrypoint
# https://github.com/vishnubob/wait-for-it/blob/master/README.md


# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput && echo "Successful collectstatic" || echo "Not successful collectstatic"

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate && echo "Successful migrate" || echo "Not successful migrate"

# Start server
echo "Starting server"
gunicorn core.wsgi:application --bind 0.0.0.0:8000