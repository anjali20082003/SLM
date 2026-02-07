# Software & License Management (SLM)

Enterprise-ready Django web application for managing software assets, licenses, AMC/support contracts, renewals, vendors, invoices, payments, and compliance across departments.

## Features

- **Asset Registry**: Full CRUD, categorization, tags, advanced search, soft delete, bulk import/export
- **License Allocation**: Track available vs used licenses, prevent over-allocation, department-wise views
- **Renewal Automation**: Celery + Redis background jobs for status updates, reminders, escalation
- **Notifications**: Email, in-app alerts, WebSocket real-time updates, custom reminder schedules
- **Dashboards**: IT, Finance, Management views with charts and KPIs
- **Reports**: Software inventory, renewal calendar, vendor spend, audit trail (API/JSON)
- **RBAC**: Super Admin, IT Manager, IT Staff, Finance Manager, Accounts Officer, Department Head, Auditor (read-only)
- **Security**: JWT auth, 2FA (django-otp), encryption for sensitive fields, audit logging, rate limiting
- **API**: REST with drf-spectacular (OpenAPI/Swagger)

## Quick Start

### Local (SQLite, minimal – no Celery/Channels)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements-minimal.txt
set DJANGO_ENV=minimal
set DJANGO_SETTINGS_MODULE=config.settings
python manage.py migrate
python manage.py createsuperuser   # use email as username
python manage.py runserver
```

Open http://127.0.0.1:8000 and sign in. Create departments/branches and users from Django Admin (/admin/).

### Full stack (Celery, Redis, Channels)

```bash
pip install -r requirements.txt
# Set DB_* and CELERY_BROKER_URL if using PostgreSQL/Redis
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# In another terminal: celery -A config worker -l info
# Optional: celery -A config beat -l info
```

### Docker

```bash
cp .env.example .env
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Web: http://localhost:8000. API docs: http://localhost:8000/api/schema/swagger-ui/

### API (JWT)

```bash
# Obtain token
curl -X POST http://localhost:8000/api/auth/token/ -H "Content-Type: application/json" -d "{\"email\":\"your@email.com\",\"password\":\"yourpass\"}"
# Use in headers: Authorization: Bearer <access_token>
```

## Project Structure

- `config/` – Django settings, URLs, Celery, ASGI
- `slm/` – Main app: models (user, software, vendor, invoice, audit, notification), API, views, tasks, middleware, permissions
- `templates/` – Base and SLM templates (Tailwind)
- `requirements.txt` – Dependencies

## User Roles

| Role | Access |
|------|--------|
| Super Admin | Full access |
| IT Manager | Assets, contracts, allocations, approve |
| IT Staff | Assets, contracts, allocations (edit) |
| Finance Manager | Vendors, invoices, payments, approve |
| Accounts Officer | Vendors, invoices, payments |
| Department Head | Department view, approve |
| Auditor | Read-only (all modules) |

## Celery Tasks

- `check_renewals_due` – Mark contracts as pending_renewal (daily 8 AM)
- `update_expired_contracts` – Set expired status (daily 0:30)
- `send_renewal_reminders` – In-app + email reminders (daily 9 AM)

## Deployment

For deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## License

MIT.
