"""Notifications and reminder schedules."""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """In-app notification."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50, blank=True)  # renewal_due, expiry, etc.

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} -> {self.user.email}"


class ReminderSchedule(models.Model):
    """Custom reminder schedule (e.g. 30 days before renewal)."""
    FREQUENCIES = [
        ("days_before", "Days before due"),
        ("weekly", "Weekly"),
        ("daily", "Daily"),
    ]
    name = models.CharField(max_length=100)
    days_before_due = models.PositiveIntegerField(default=30, help_text="Notify this many days before renewal/expiry")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["days_before_due"]

    def __str__(self):
        return f"{self.name} ({self.days_before_due} days before)"
