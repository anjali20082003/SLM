"""Vendor model."""
from django.db import models
from slm.encryption import encrypt_value, decrypt_value


class Vendor(models.Model):
    """Vendor/supplier for software and invoices."""
    company_name = models.CharField(max_length=300)
    contact_person = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # e.g. 1-5
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["company_name"]

    def __str__(self):
        return self.company_name
