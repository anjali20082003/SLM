"""Django admin for SLM."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Department, Branch,
    SoftwareAsset, LicenseContract, Allocation, RenewalHistory,
    Vendor, Invoice, Payment,
    AuditLog, Notification, ReminderSchedule,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "department", "is_active")
    list_filter = ("role", "is_active", "department")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ()
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("role", "department", "branch", "phone", "is_verified")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "role", "department")}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "branch", "is_active")
    list_filter = ("branch", "is_active")
    search_fields = ("name", "code")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    list_filter = ("is_active",)


@admin.register(SoftwareAsset)
class SoftwareAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "version", "license_type", "total_licenses", "is_deleted", "updated_at")
    list_filter = ("license_type", "category", "is_deleted")
    search_fields = ("name", "description", "tags")
    readonly_fields = ("created_at", "updated_at")


@admin.register(LicenseContract)
class LicenseContractAdmin(admin.ModelAdmin):
    list_display = ("software_asset", "vendor", "purchase_date", "expiry_date", "renewal_due_date", "status", "support_level")
    list_filter = ("status", "support_level")
    search_fields = ("software_asset__name",)
    date_hierarchy = "expiry_date"


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ("software_asset", "department", "user", "allocated_on", "active_flag")
    list_filter = ("active_flag", "department")
    search_fields = ("software_asset__name", "user__email")


@admin.register(RenewalHistory)
class RenewalHistoryAdmin(admin.ModelAdmin):
    list_display = ("license_contract", "previous_expiry", "new_expiry", "renewed_by", "timestamp")
    list_filter = ("timestamp",)
    readonly_fields = ("timestamp",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_person", "email", "rating", "is_active")
    list_filter = ("is_active",)
    search_fields = ("company_name", "contact_person")


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "vendor", "invoice_date", "total", "currency")
    list_filter = ("currency",)
    search_fields = ("invoice_number",)
    inlines = [PaymentInline]
    date_hierarchy = "invoice_date"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "payment_mode", "paid_on")
    list_filter = ("payment_mode",)
    date_hierarchy = "paid_on"


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("entity", "change_type", "user", "ip_address", "timestamp")
    list_filter = ("change_type", "entity")
    search_fields = ("entity", "user__email")
    readonly_fields = ("timestamp",)
    date_hierarchy = "timestamp"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_read", "created_at")
    list_filter = ("is_read", "notification_type")


@admin.register(ReminderSchedule)
class ReminderScheduleAdmin(admin.ModelAdmin):
    list_display = ("name", "days_before_due", "is_active")
