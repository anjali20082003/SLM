"""SoftwareAsset, LicenseContract, Allocation, RenewalHistory."""
from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

from .user import Department, User
from .vendor import Vendor


class SoftwareAsset(models.Model):
    """Software asset registry."""
    LICENSE_TYPES = [
        ("perpetual", "Perpetual"),
        ("subscription", "Subscription"),
        ("concurrent", "Concurrent"),
        ("device", "Per Device"),
        ("user", "Per User"),
    ]
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=100, blank=True, db_index=True)
    version = models.CharField(max_length=100, blank=True)
    license_type = models.CharField(max_length=30, choices=LICENSE_TYPES, default="subscription")
    total_licenses = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    is_deleted = models.BooleanField(default=False, db_index=True)  # Soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_assets"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Software assets"

    def __str__(self):
        return f"{self.name} ({self.version or 'N/A'})"

    @property
    def used_licenses(self):
        return self.allocations.filter(active_flag=True).count()

    @property
    def available_licenses(self):
        return max(0, self.total_licenses - self.used_licenses)

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class LicenseContract(models.Model):
    """License contract linked to software and vendor."""
    STATUS_CHOICES = [
        ("active", "Active"),
        ("expired", "Expired"),
        ("pending_renewal", "Pending Renewal"),
        ("cancelled", "Cancelled"),
    ]
    SUPPORT_LEVELS = [
        ("standard", "Standard"),
        ("premium", "Premium"),
        ("enterprise", "Enterprise"),
        ("none", "None"),
    ]
    software_asset = models.ForeignKey(
        SoftwareAsset, on_delete=models.CASCADE, related_name="contracts"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name="contracts"
    )
    purchase_date = models.DateField()
    duration_months = models.PositiveIntegerField(default=12)
    expiry_date = models.DateField(null=True, blank=True)  # Can be auto-calculated
    renewal_due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="active", db_index=True)
    support_level = models.CharField(max_length=30, choices=SUPPORT_LEVELS, default="standard")
    contract_document = models.FileField(upload_to="contracts/%Y/%m/", blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-expiry_date", "-renewal_due_date"]

    def __str__(self):
        return f"{self.software_asset.name} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.expiry_date and self.purchase_date and self.duration_months:
            from dateutil.relativedelta import relativedelta
            self.expiry_date = self.purchase_date + relativedelta(months=self.duration_months)
        if not self.renewal_due_date and self.expiry_date:
            from dateutil.relativedelta import relativedelta
            self.renewal_due_date = self.expiry_date - relativedelta(days=30)
        super().save(*args, **kwargs)


class Allocation(models.Model):
    """License allocation to department/user."""
    software_asset = models.ForeignKey(
        SoftwareAsset, on_delete=models.CASCADE, related_name="allocations"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="allocations"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="allocations", null=True, blank=True
    )
    allocated_on = models.DateTimeField(default=timezone.now)
    returned_on = models.DateTimeField(null=True, blank=True)
    active_flag = models.BooleanField(default=True, db_index=True)
    notes = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-allocated_on"]
        # One allocation per user per asset when user is set; user can be null for pool

    def __str__(self):
        u = self.user.email if self.user else "Unassigned"
        return f"{self.software_asset.name} -> {self.department.code} / {u}"

    def save(self, *args, **kwargs):
        if self.returned_on:
            self.active_flag = False
        super().save(*args, **kwargs)


class RenewalHistory(models.Model):
    """History of renewals for audit."""
    license_contract = models.ForeignKey(
        LicenseContract, on_delete=models.CASCADE, related_name="renewal_history"
    )
    previous_expiry = models.DateField(null=True, blank=True)
    new_expiry = models.DateField()
    invoice = models.ForeignKey(
        "slm.Invoice", on_delete=models.SET_NULL, null=True, blank=True, related_name="renewals"
    )
    renewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="renewals"
    )
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Renewal history"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.license_contract} renewed on {self.timestamp.date()}"
