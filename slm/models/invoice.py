"""Invoice and Payment models."""
from django.db import models
from django.conf import settings
from decimal import Decimal

from .vendor import Vendor

# LicenseContract imported via string in FK to avoid circular import

CURRENCY_CHOICES = [
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("GBP", "GBP"),
    ("INR", "INR"),
    ("OTHER", "Other"),
]


class Invoice(models.Model):
    """Invoice linked to vendor and optionally contract."""
    invoice_number = models.CharField(max_length=100, db_index=True)
    invoice_date = models.DateField()
    file_upload = models.FileField(upload_to="invoices/%Y/%m/", blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name="invoices"
    )
    license_contract = models.ForeignKey(
        "slm.LicenseContract", on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices"
    )
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0"))
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0"))
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="USD")
    total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0"))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_invoices"
    )

    class Meta:
        ordering = ["-invoice_date"]

    def __str__(self):
        return f"{self.invoice_number} - {self.total} {self.currency}"

    def save(self, *args, **kwargs):
        if self.subtotal is not None and self.tax is not None:
            self.total = self.subtotal + self.tax
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment against invoice."""
    PAYMENT_MODES = [
        ("bank_transfer", "Bank Transfer"),
        ("cheque", "Cheque"),
        ("card", "Card"),
        ("upi", "UPI"),
        ("other", "Other"),
    ]
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )
    payment_mode = models.CharField(max_length=30, choices=PAYMENT_MODES)
    transaction_reference = models.CharField(max_length=200, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    paid_on = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="payments_created"
    )

    class Meta:
        ordering = ["-paid_on"]

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.amount} on {self.paid_on}"
