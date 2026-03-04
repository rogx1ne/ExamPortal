#!/usr/bin/env sh
set -eu

python /app/scripts/wait_for_db.py

python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput

exec gunicorn exam_portal.wsgi:application --bind 0.0.0.0:8000 --workers "${WEB_CONCURRENCY:-3}"
