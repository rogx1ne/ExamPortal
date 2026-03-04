# Demo Script (Invigilator Walkthrough)

This project includes a demo seeder so you can show the full flow quickly (Admin + Student).

## 1) Seed demo data

### Docker

```bash
docker compose exec web python manage.py seed_demo
```

### Local (venv)

```bash
python manage.py seed_demo
```

Default demo credentials:

- Admin: `admin_demo` / `Admin@12345`
- Student: `student_demo` / `Student@12345`

## 2) Admin walkthrough (2–3 minutes)

1) Login as Admin: `/accounts/login/`
2) Open Dashboard: `/accounts/dashboard/`
3) Show **Manage Exams**:
   - View seeded exams (including an inactive one)
   - Toggle active/inactive on the "DEMO - Inactive Exam (Toggle Demo)"
4) Open **Questions** for an exam and show add/edit/delete question.
5) Open **Student Results** and point out:
   - Attempts count
   - Average score/percentage

## 3) Student walkthrough (2–3 minutes)

1) Login as Student: `/accounts/login/`
2) Open **Exams**: `/exams/`
3) Start "DEMO - Python Basics (MCQ)" and submit.
4) Open **Results**: `/results/` and show:
   - Score + percentage
   - Per-question review
5) Try opening the same exam again to show **single attempt** enforcement.

## 4) Quick non-UI checks (optional)

- Health endpoint: `/_health/` (returns JSON)

