"""Serializers for SLM API."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from slm.models import (
    Department, Branch,
    SoftwareAsset, LicenseContract, Allocation, RenewalHistory,
    Vendor, Invoice, Payment,
    AuditLog, Notification,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "department", "branch")
        read_only_fields = ("id", "email")


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class SoftwareAssetSerializer(serializers.ModelSerializer):
    used_licenses = serializers.ReadOnlyField()
    available_licenses = serializers.ReadOnlyField()

    class Meta:
        model = SoftwareAsset
        fields = (
            "id", "name", "category", "version", "license_type", "total_licenses",
            "description", "tags", "is_deleted", "used_licenses", "available_licenses",
            "created_at", "updated_at", "created_by"
        )
        read_only_fields = ("created_at", "updated_at")


class LicenseContractSerializer(serializers.ModelSerializer):
    software_asset_name = serializers.CharField(source="software_asset.name", read_only=True)
    vendor_name = serializers.CharField(source="vendor.company_name", read_only=True, allow_null=True)

    class Meta:
        model = LicenseContract
        fields = (
            "id", "software_asset", "software_asset_name", "vendor", "vendor_name",
            "purchase_date", "duration_months", "expiry_date", "renewal_due_date",
            "status", "support_level", "contract_document", "notes",
            "created_at", "updated_at"
        )
        read_only_fields = ("expiry_date", "created_at", "updated_at")


class AllocationSerializer(serializers.ModelSerializer):
    software_asset_name = serializers.CharField(source="software_asset.name", read_only=True)
    department_code = serializers.CharField(source="department.code", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True, allow_null=True)

    class Meta:
        model = Allocation
        fields = (
            "id", "software_asset", "software_asset_name", "department", "department_code",
            "user", "user_email", "allocated_on", "returned_on", "active_flag", "notes",
            "created_at", "updated_at"
        )
        read_only_fields = ("created_at", "updated_at")


class RenewalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RenewalHistory
        fields = "__all__"
        read_only_fields = ("timestamp",)


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("created_at",)


class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id", "invoice_number", "invoice_date", "file_upload", "vendor", "license_contract",
            "subtotal", "tax", "currency", "total", "notes", "payments",
            "created_at", "updated_at", "created_by"
        )
        read_only_fields = ("created_at", "updated_at")


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True, allow_null=True)

    class Meta:
        model = AuditLog
        fields = ("id", "entity", "object_id", "change_type", "old_value", "new_value", "user", "user_email", "ip_address", "timestamp", "extra")
        read_only_fields = fields


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "link", "is_read", "notification_type", "created_at")
        read_only_fields = ("created_at",)
