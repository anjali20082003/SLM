"""Report API endpoints - return JSON or trigger export."""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from slm.models import SoftwareAsset, LicenseContract, Invoice, AuditLog, Allocation
from slm.permissions import SLMPermission


class ReportInventoryView(APIView):
    permission_classes = [SLMPermission]

    def get(self, request):
        data = list(SoftwareAsset.objects.filter(is_deleted=False).values(
            "id", "name", "category", "version", "license_type", "total_licenses"
        ))
        for a in data:
            a["used"] = Allocation.objects.filter(software_asset_id=a["id"], active_flag=True).count()
        return Response({"assets": data})


class ReportRenewalCalendarView(APIView):
    permission_classes = [SLMPermission]

    def get(self, request):
        from datetime import timedelta
        from django.utils import timezone
        today = timezone.now().date()
        end = today + timedelta(days=365)
        contracts = LicenseContract.objects.filter(
            expiry_date__gte=today, expiry_date__lte=end, status="active"
        ).select_related("software_asset", "vendor").order_by("expiry_date").values(
            "id", "software_asset__name", "expiry_date", "renewal_due_date", "vendor__company_name"
        )
        return Response({"contracts": list(contracts)})


class ReportVendorSpendView(APIView):
    permission_classes = [SLMPermission]

    def get(self, request):
        from slm.models import Vendor
        spend = Invoice.objects.values("vendor").annotate(total=Sum("total")).order_by("-total")
        vendor_ids = [s["vendor"] for s in spend if s["vendor"]]
        vendors = {v.id: v.company_name for v in Vendor.objects.filter(id__in=vendor_ids)}
        data = [{"vendor_id": s["vendor"], "vendor_name": vendors.get(s["vendor"], "N/A"), "total": str(s["total"])} for s in spend]
        return Response({"vendor_spend": data})


class ReportAuditTrailView(APIView):
    permission_classes = [SLMPermission]

    def get(self, request):
        logs = AuditLog.objects.select_related("user").order_by("-timestamp")[:500].values(
            "id", "entity", "change_type", "user__email", "ip_address", "timestamp"
        )
        return Response({"audit_logs": list(logs)})
