# Online Examination Portal (Django + MySQL)

![CI](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)

> Note: replace `<OWNER>/<REPO>` in the CI badge after pushing to GitHub.

Web-based Online Examination Portal built with:

- Python (Django)
- MySQL (strictly)
- Django Templates (HTML) + Bootstrap

## Features

- Custom user model (`AbstractUser`) with roles: **Admin**, **Student**
- Admin panel (in-app):
  - Create/edit/delete exams
  - Activate/deactivate exams
  - Add/edit/delete MCQ questions
  - View all student results + exam-wise summary (avg score, attempts)
- Student portal:
  - Register/login
  - View active exams
  - Attempt exam (single attempt per exam)
  - Auto scoring + result history

## Quickstart

Common dev commands are available in `Makefile` (optional).

### Option A: Run with Docker (recommended)

Prereqs: Docker + Docker Compose.

1) Create an `.env` from the sample:

```bash
cp .env.example .env
```

2) Start services:

```bash
docker compose up --build
```

Open `http://127.0.0.1:8000/`

To create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

Health check: `http://127.0.0.1:8000/_health/`

### Option B: Run locally (venv)

Prereqs: Python 3.12+ and a MySQL server (or Docker MySQL).

#### 1) Create virtual environment & install deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional (tests/lint):

```bash
pip install -r requirements-dev.txt
```

Or use the Makefile:

```bash
make install-dev
```

#### 2) Create MySQL database

Login to MySQL and create a database/user:

```sql
CREATE DATABASE exam_portal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'exam_portal_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON exam_portal_db.* TO 'exam_portal_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 3) Configure environment variables

Set these environment variables before running (or use `.env`):

```bash
export DJANGO_SECRET_KEY="change-me"
export DJANGO_DEBUG="1"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
export DB_NAME="exam_portal_db"
export DB_USER="exam_portal_user"
export DB_PASSWORD="change_this_password"
export DB_HOST="127.0.0.1"
export DB_PORT="3306"
```

If you are using a `.env` locally, `manage.py` auto-loads it via `python-dotenv`.

### Configuration reference

| Variable | Purpose | Example |
| --- | --- | --- |
| `DJANGO_ENV` | Environment (`development`/`production`/`test`) | `development` |
| `DJANGO_DEBUG` | Django debug toggle | `1` / `0` |
| `DJANGO_SECRET_KEY` | Django secret key | `change-me` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts (comma-separated) | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | CSRF trusted origins (comma-separated) | `https://example.com` |
| `DJANGO_HEALTHCHECK_DB` | If `1`, `/_health/` also pings DB | `1` |
| `DB_NAME` | MySQL database name | `exam_portal_db` |
| `DB_USER` | MySQL user | `exam_portal_user` |
| `DB_PASSWORD` | MySQL password | `...` |
| `DB_HOST` | MySQL host | `127.0.0.1` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_WAIT_SECONDS` | Docker DB wait timeout | `60` |

#### 4) Run migrations

```bash
python manage.py migrate
```

#### 5) Create Admin user

Create a Django superuser (this becomes an **Admin** in the portal):

```bash
python manage.py createsuperuser
```

#### 6) Start server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`

### Option C: Run on Windows (no Docker)

Prereqs: Python 3.12+ and a MySQL server (or use Docker for MySQL only).

1) Create and activate venv (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```powershell
pip install -r requirements.txt -r requirements-dev.txt
```

> Note: `gunicorn` is automatically skipped on Windows via a dependency marker.

3) Create a `.env` (recommended):

```powershell
copy .env.example .env
```

Edit `.env` with your DB credentials. `manage.py` auto-loads `.env`.

4) Run migrations + start server:

```powershell
python manage.py migrate
python manage.py runserver
```

Optional cross-platform task runner:

```powershell
python scripts\tasks.py demo
python scripts\tasks.py test --cov
```

## Demo (invigilator-ready)

Seed demo users/exams/questions/results (idempotent):

```bash
python manage.py seed_demo
```

Docker:

```bash
docker compose exec web python manage.py seed_demo
```

Default demo credentials:

- Admin: `admin_demo` / `Admin@12345`
- Student: `student_demo` / `Student@12345`

Walkthrough script: `DEMO.md`.

## Development

Recommended:

```bash
make install-dev
make format
make lint
make test
```

Pre-commit hooks:

```bash
pre-commit install
pre-commit run --all-files
```

CI runs `ruff` + `pytest` + coverage on every push/PR.

### Useful commands

- Docker up/down: `make docker-up`, `make docker-down`
- Seed demo data: `make demo`
- Lint/format: `ruff check .`, `ruff format .`
- Tests: `pytest`
- Cross-platform tasks (Windows-friendly): `python scripts/tasks.py lint|format|test|demo|runserver`

## Project structure

```
exam_portal/   Django project (settings/urls/wsgi/asgi, custom admin site, health endpoint)
accounts/      Custom user model + roles (Admin/Student), auth views, dashboards, decorators
exams/         Exams domain (models/forms/views), in-app admin panel, demo seeder command
templates/     Django templates (Bootstrap UI)
static/        Static assets (dev)
staticfiles/   Collected static output (prod; created by collectstatic)
scripts/       Docker entrypoint + DB wait helper
tests/         pytest tests (SQLite in-memory via settings_test)
```

## Production notes

- Set `DJANGO_DEBUG=0` and provide `DJANGO_SECRET_KEY` + `DJANGO_ALLOWED_HOSTS`.
- Set `DJANGO_CSRF_TRUSTED_ORIGINS` if serving behind a different domain.
- Static files are served via `whitenoise` (run `python manage.py collectstatic` during build/deploy).
- Consider enabling these only after HTTPS is confirmed:
  - `DJANGO_SECURE_SSL_REDIRECT=1`
  - `DJANGO_SECURE_HSTS_SECONDS=31536000`
- Use `LOG_LEVEL` via `DJANGO_LOG_LEVEL` in production (default `INFO`).

## Notes

- MySQL is configured in `exam_portal/settings.py`.
- This project uses `PyMySQL` (pure Python) as the MySQL driver for easier setup. If you prefer `mysqlclient`, install it and remove `PyMySQL`.
- Students cannot access Django admin (`/admin/`) because the admin site permission check enforces `role=ADMIN`.
- Students can attempt an exam only once (enforced via a unique constraint).
