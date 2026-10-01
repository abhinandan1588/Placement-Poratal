# Placement Portal Application (PPA)

A campus placement management platform for three roles — **Admin (Institute)**,
**Company**, and **Student**. Built with Flask (REST API), Vue 2 (CLI), SQLite,
Redis caching, and Celery for batch jobs.

## Tech stack

| Layer      | Technology                                  |
|------------|---------------------------------------------|
| Backend    | Flask, Flask-JWT-Extended, Flask-SQLAlchemy |
| Frontend   | Vue 2 (Vue CLI), Vue Router, Vuex, Bootstrap 5, Chart.js |
| Database   | SQLite (created programmatically)           |
| Caching    | Redis (Flask-Caching) with in-memory fallback |
| Batch jobs | Celery + Redis (worker & beat)              |

## Project structure

```
mad2/
├── backend/
│   ├── app.py              # App factory, schema creation, admin seeding
│   ├── config.py           # Configuration
│   ├── extensions.py       # db, jwt, cache, cors
│   ├── models.py           # User, StudentProfile, CompanyProfile, PlacementDrive, Application
│   ├── utils.py            # Role guards, eligibility checks
│   ├── celery_app.py       # Celery instance + beat schedule
│   ├── celery_worker.py    # Worker/beat entrypoint
│   ├── tasks.py            # Daily reminders, monthly report, CSV export
│   ├── resources/          # auth / admin / company / student blueprints
│   ├── seed_demo.py        # Optional sample data
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── views/          # Home, Login, Register, admin/, company/, student/
    │   ├── components/     # Navbar, Toast, StatCard, BarChart
    │   ├── router/ store/ services/
    └── package.json
```

## Prerequisites

- Python 3.10+ (tested on 3.14)
- Node.js 18+ (tested on 24) and npm
- Redis (optional for a basic demo — see note below)

> **Redis on Windows:** Redis has no official Windows build. Use one of:
> WSL (`sudo apt install redis-server`), Docker (`docker run -p 6379:6379 redis`),
> or Memurai. Without Redis the API still runs (caching falls back to an
> in-memory store), but Celery jobs require a running Redis broker.

## Backend setup

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py            # starts API at http://localhost:5000
```

On first run the SQLite schema is created automatically and the **admin** user
is seeded:

```
admin@ppa.com / admin123
```

Optional sample data (companies, students, drives, applications):

```powershell
python seed_demo.py
```

Demo logins after seeding:

| Role    | Email             | Password    |
|---------|-------------------|-------------|
| Admin   | admin@ppa.com     | admin123    |
| Company | hr@technova.com   | company123  |
| Student | aarav@uni.com     | student123  |

## Frontend setup

```powershell
cd frontend
npm install
npm run serve            # dev server at http://localhost:8080
```

The dev server proxies `/api` to `http://localhost:5000`, so run the backend
alongside it. For a production bundle: `npm run build`.

## Background jobs (Celery)

Requires Redis running. In separate terminals (inside `backend/` with the venv
activated):

```powershell
REM Worker (Windows needs the solo pool)
celery -A celery_worker.celery worker --loglevel=info --pool=solo

REM Scheduler for daily/monthly jobs
celery -A celery_worker.celery beat --loglevel=info
```

Convenience scripts are provided: `run_server.bat`, `run_celery_worker.bat`,
`run_celery_beat.bat`.

### Jobs implemented

1. **Daily reminders** (`tasks.send_daily_reminders`, 09:00 daily) — emails /
   Google-Chat reminders to students about drives closing within 3 days.
2. **Monthly activity report** (`tasks.send_monthly_report`, 1st of month
   08:00) — HTML report of drives, applications and selections, emailed to admin.
3. **CSV export** (`tasks.export_applications_csv`, user triggered) — a student
   exports their application history; the file is generated asynchronously and
   they are notified when ready.

> If `MAIL_SERVER` is not configured, emails are printed to the worker console
> so the jobs are fully demoable without mail credentials.

### Trigger a job manually for a demo

```powershell
venv\Scripts\activate
python -c "import celery_worker, tasks; print(tasks.send_daily_reminders.delay().get(timeout=30))"
python -c "import celery_worker, tasks; print(tasks.send_monthly_report.delay().get(timeout=30))"
```
## Install MailHog
    WSL (Windows Users)
    sudo apt update
    sudo apt install -y golang-go
    go install github.com/mailhog/MailHog@latest
##          for using 
    ~/go/bin/MailHog
## Core features

**Authentication & roles** — unified `User` model, JWT auth, role-based route
guards. Students and companies self-register; admin is pre-seeded (no admin
registration).

**Admin** — dashboard counts, approve/reject companies and drives, search
students and companies, blacklist/deactivate accounts, reports with charts.

**Company** — profile, dashboard, create drives (only after approval), view
applicants per drive, shortlist/select/reject, schedule interviews.

**Student** — profile + resume upload, browse approved drives with
eligibility-based filtering and search, apply (with duplicate-apply and
eligibility validation), application status, placement history, CSV export.

**Performance** — admin dashboard stats cached in Redis (60s expiry) and
invalidated on relevant writes.

## Configuration

Copy `backend/.env.example` to `backend/.env` to override defaults (secrets,
admin credentials, Redis URLs, mail settings, Google Chat webhook).

## API quick reference

| Method | Endpoint                                   | Role    |
|--------|--------------------------------------------|---------|
| POST   | /api/auth/register/student                 | public  |
| POST   | /api/auth/register/company                 | public  |
| POST   | /api/auth/login                            | public  |
| GET    | /api/admin/dashboard                       | admin   |
| GET/PATCH | /api/admin/companies[/:id/approval]     | admin   |
| GET    | /api/admin/students                        | admin   |
| PATCH  | /api/admin/users/:id/status                | admin   |
| GET/PATCH | /api/admin/drives[/:id/approval]        | admin   |
| GET    | /api/admin/reports                         | admin   |
| GET/PUT | /api/company/profile                      | company |
| GET/POST | /api/company/drives                      | company |
| GET    | /api/company/drives/:id/applications       | company |
| PATCH  | /api/company/applications/:id              | company |
| GET    | /api/student/drives                         | student |
| POST   | /api/student/drives/:id/apply              | student |
| GET    | /api/student/applications                   | student |
| POST   | /api/student/export                         | student |
| POST   | /api/student/resume                         | student |
```
