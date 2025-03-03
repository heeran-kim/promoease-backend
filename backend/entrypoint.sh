#!/bin/sh

set -e  # Exit immediately if a command fails

echo "Making database migrations..."
python manage.py makemigrations --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Flushing database..."
python manage.py flush --noinput

echo "Loading fixture data..."
python manage.py loaddata users/fixtures/mock_users.json businesses/fixtures/mock_businesses.json social/fixtures/mock_social.json posts/fixtures/mock_posts.json promotions/fixtures/mock_promotions.json

echo "Starting server with HTTPS..."
exec python manage.py runserver_plus --cert-file /app/localhost.pem --key-file /app/localhost-key.pem 0.0.0.0:8000
