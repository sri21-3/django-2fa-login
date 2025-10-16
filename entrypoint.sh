#!/usr/bin/env sh
set -e

# Wait for Postgres
echo "Waiting for Postgres at ${DB_HOST:-db}:${DB_PORT:-5432}..."
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}" >/dev/null 2>&1; do
  sleep 1
done
echo "Postgres is ready."

# Create and apply migrations, then collect static files (idempotent)
python manage.py makemigrations authentication || true
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3}


