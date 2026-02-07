"""Celery configuration for renewal automation and background tasks."""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Renewal checks: daily at 8 AM
app.conf.beat_schedule = {
    "renewal-due-check": {
        "task": "slm.tasks.check_renewals_due",
        "schedule": crontab(hour=8, minute=0),
    },
    "expiry-status-update": {
        "task": "slm.tasks.update_expired_contracts",
        "schedule": crontab(hour=0, minute=30),
    },
    "send-renewal-reminders": {
        "task": "slm.tasks.send_renewal_reminders",
        "schedule": crontab(hour=9, minute=0),
    },
}
