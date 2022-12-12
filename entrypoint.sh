#!/bin/sh

echo "Running collectstatic..."
python3 manage.py collectstatic --no-input --settings=premiosplatziapp.settings.production

echo "Appliying migrations..."
python3 manage.py wait_for_db --settings=premiosplatziapp.settings.production
python3 manage.py migrate --settings=premiosplatziapp.settings.production

echo "Running server..."
gunicorn --env DJANGO_SETTINGS_MODULE=premiosplatziapp.settings.production premiosplatziapp.wsgi:application --bind 0.0.0.0:8000