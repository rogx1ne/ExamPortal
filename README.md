# Online Examination Portal (Django + MySQL)

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

## Setup

### 1) Create virtual environment & install deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Create MySQL database

Login to MySQL and create a database/user:

```sql
CREATE DATABASE exam_portal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'exam_portal_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON exam_portal_db.* TO 'exam_portal_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3) Configure environment variables

Set these environment variables (recommended) before running:

```bash
export DJANGO_SECRET_KEY="change-me"
export DJANGO_DEBUG="1"
export DB_NAME="exam_portal_db"
export DB_USER="exam_portal_user"
export DB_PASSWORD="change_this_password"
export DB_HOST="127.0.0.1"
export DB_PORT="3306"
```

### 4) Run migrations

```bash
python manage.py migrate
```

### 5) Create Admin user

Create a Django superuser (this becomes an **Admin** in the portal):

```bash
python manage.py createsuperuser
```

### 6) Start server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`

## Notes

- MySQL is configured in `exam_portal/settings.py`.
- This project uses `PyMySQL` (pure Python) as the MySQL driver for easier setup. If you prefer `mysqlclient`, install it and remove `PyMySQL`.
- Students cannot access Django admin (`/admin/`) because the admin site permission check enforces `role=ADMIN`.
- Students can attempt an exam only once (enforced via a unique constraint).
