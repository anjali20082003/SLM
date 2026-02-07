"""Forms for SLM create/edit."""
from django import forms
from django.contrib.auth import get_user_model

from .models import (
    SoftwareAsset,
    LicenseContract,
    Allocation,
    Vendor,
    Invoice,
    Payment,
    Department,
    Branch,
)

User = get_user_model()


class SoftwareAssetForm(forms.ModelForm):
    class Meta:
        model = SoftwareAsset
        fields = [
            "name", "category", "version", "license_type", "total_licenses",
            "description", "tags",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "category": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "version": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "license_type": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "total_licenses": forms.NumberInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "min": 0}),
            "description": forms.Textarea(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "rows": 3}),
            "tags": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "placeholder": "tag1, tag2"}),
        }


class LicenseContractForm(forms.ModelForm):
    class Meta:
        model = LicenseContract
        fields = [
            "software_asset", "vendor", "purchase_date", "duration_months",
            "expiry_date", "renewal_due_date", "status", "support_level", "contract_document", "notes",
        ]
        widgets = {
            "software_asset": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "vendor": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "purchase_date": forms.DateInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "type": "date"}),
            "duration_months": forms.NumberInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "min": 1}),
            "expiry_date": forms.DateInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "type": "date"}),
            "renewal_due_date": forms.DateInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "type": "date"}),
            "status": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "support_level": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "contract_document": forms.FileInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "notes": forms.Textarea(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "rows": 2}),
        }


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["company_name", "contact_person", "email", "phone", "rating", "address", "is_active"]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "contact_person": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "email": forms.EmailInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "phone": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "rating": forms.NumberInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "step": "0.01", "min": 0, "max": 5}),
            "address": forms.Textarea(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "rows": 2}),
            "is_active": forms.CheckboxInput(attrs={"class": "rounded border-gray-300 dark:border-gray-600"}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["invoice", "payment_mode", "transaction_reference", "bank_name", "amount", "paid_on", "notes"]
        widgets = {
            "invoice": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "payment_mode": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "transaction_reference": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "bank_name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "amount": forms.NumberInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "step": "0.01"}),
            "paid_on": forms.DateInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "rows": 2}),
        }


class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ["software_asset", "department", "user", "notes", "returned_on", "active_flag"]
        widgets = {
            "software_asset": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "department": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "user": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "notes": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "returned_on": forms.DateInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "type": "date"}),
            "active_flag": forms.CheckboxInput(attrs={"class": "rounded border-gray-300 dark:border-gray-600"}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "invoice_number", "invoice_date", "file_upload", "vendor", "license_contract",
            "subtotal", "tax", "currency", "notes",
        ]
        widgets = {
            "invoice_number": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "invoice_date": forms.DateInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "type": "date"}),
            "file_upload": forms.FileInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "vendor": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "license_contract": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "subtotal": forms.NumberInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "step": "0.01"}),
            "tax": forms.NumberInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "step": "0.01"}),
            "currency": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "notes": forms.Textarea(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "rows": 2}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "branch"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "code": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "branch": forms.Select(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
        }


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "code", "address", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "code": forms.TextInput(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2"}),
            "address": forms.Textarea(attrs={"class": "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2", "rows": 2}),
            "is_active": forms.CheckboxInput(attrs={"class": "rounded border-gray-300 dark:border-gray-600"}),
        }
