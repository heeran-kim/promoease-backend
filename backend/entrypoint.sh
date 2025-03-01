#!/bin/sh

set -e  # Exit immediately if a command fails

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Flushing database..."
python manage.py flush --noinput

echo "Loading fixture data..."
python manage.py loaddata users/fixtures/mock_users.json businesses/fixtures/mock_businesses.json social/fixtures/mock_social.json posts/fixtures/mock_posts.json

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
