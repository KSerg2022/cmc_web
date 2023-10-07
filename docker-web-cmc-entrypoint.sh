#!/bin/bash

# https://stackoverflow.com/questions/52942913/docker-compose-docker-entrypoint
# https://github.com/vishnubob/wait-for-it/blob/master/README.md

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput && echo "Successful collectstatic" || echo "Not successful collectstatic"

# Apply database makemigrations
echo "Apply database makemigrations"
python manage.py makemigrations && echo "Successful makemigrations" || echo "Not successful makemigrations"

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate && echo "Successful migrate" || echo "Not successful migrate"

# Apply fixtures exchanger
echo "Apply fixtures exchanger"
python manage.py loaddata data/fixtures/exchanger.json && echo "Successful loaded exchanger" || echo "Not loaded exchanger"

# Apply fixtures blockchain
echo "Apply fixtures blockchain"
python manage.py loaddata data/fixtures/blockchain.json && echo "Successful loaded blockchain" || echo "Not loaded blockchain"

# Apply fixtures cryptocurrency
echo "Apply fixtures cryptocurrency"
python manage.py loaddata data/fixtures/cryptocurrency.json && echo "Successful loaded cryptocurrency" || echo "Not loaded cryptocurrency"

# Apply create superuser
echo "Apply create superuser"
python manage.py createsuperuser --noinput && echo "Successful created superuser" || echo "Not created superuser"

# Start server
echo "Starting server"
gunicorn core.wsgi:application --bind 0.0.0.0:8000
