"""Celery tasks for renewal automation and notifications."""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

from slm.models import LicenseContract, RenewalHistory, Notification, ReminderSchedule
from slm.models import User


@shared_task
def check_renewals_due():
    """Mark contracts as pending_renewal when renewal_due_date is near."""
    today = timezone.now().date()
    due_soon = today + timedelta(days=30)
    LicenseContract.objects.filter(
        status="active",
        renewal_due_date__lte=due_soon,
        renewal_due_date__gte=today,
    ).update(status="pending_renewal")
    return "Renewals due check completed"


@shared_task
def update_expired_contracts():
    """Set status to expired for contracts past expiry_date."""
    today = timezone.now().date()
    LicenseContract.objects.filter(
        status__in=("active", "pending_renewal"),
        expiry_date__lt=today,
    ).update(status="expired")
    return "Expired contracts updated"


@shared_task
def send_renewal_reminders():
    """Create in-app notifications and send emails for upcoming renewals."""
    today = timezone.now().date()
    schedules = ReminderSchedule.objects.filter(is_active=True)
    created = 0
    for schedule in schedules:
        target_date = today + timedelta(days=schedule.days_before_due)
        contracts = LicenseContract.objects.filter(
            status="active",
            renewal_due_date=target_date,
        ).select_related("software_asset")
        managers = User.objects.filter(role__in=("it_manager", "finance_manager", "super_admin"))
        for contract in contracts:
            title = f"Renewal due: {contract.software_asset.name}"
            message = f"License for {contract.software_asset.name} is due for renewal on {contract.renewal_due_date}."
            for user in managers:
                Notification.objects.create(
                    user=user,
                    title=title,
                    message=message,
                    notification_type="renewal_due",
                    link=f"/contracts/?id={contract.id}",
                )
                created += 1
            try:
                send_mail(
                    subject=f"[SLM] {title}",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[e for e in [u.email for u in managers] if e],
                    fail_silently=True,
                )
            except Exception:
                pass
    return f"Created {created} reminders"
