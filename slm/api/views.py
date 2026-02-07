"""API ViewSets for SLM."""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum, Count, Q

from slm.models import (
    SoftwareAsset, LicenseContract, Allocation, RenewalHistory,
    Vendor, Invoice, Payment, AuditLog, Notification,
)
from slm.api.serializers import (
    SoftwareAssetSerializer, LicenseContractSerializer, AllocationSerializer,
    RenewalHistorySerializer, VendorSerializer, InvoiceSerializer, PaymentSerializer,
    AuditLogSerializer, NotificationSerializer,
)
from slm.permissions import SLMPermission, CanEditAssets, CanEditFinance


class SoftwareAssetViewSet(viewsets.ModelViewSet):
    queryset = SoftwareAsset.objects.filter(is_deleted=False).select_related("created_by")
    serializer_class = SoftwareAssetSerializer
    permission_classes = [SLMPermission, CanEditAssets]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "license_type"]
    search_fields = ["name", "description", "tags", "version"]
    ordering_fields = ["name", "total_licenses", "updated_at"]
    ordering = ["name"]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted", "updated_at"])

    @action(detail=False, methods=["post"])
    def bulk_import(self, request):
        # Placeholder: parse Excel/CSV and create assets
        return Response({"detail": "Use web upload for bulk import."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def export(self, request):
        # Placeholder: return CSV/Excel
        return Response({"detail": "Use web export."}, status=status.HTTP_400_BAD_REQUEST)


class LicenseContractViewSet(viewsets.ModelViewSet):
    queryset = LicenseContract.objects.select_related("software_asset", "vendor")
    serializer_class = LicenseContractSerializer
    permission_classes = [SLMPermission, CanEditAssets]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "support_level"]
    ordering_fields = ["expiry_date", "renewal_due_date", "purchase_date"]
    ordering = ["-expiry_date"]

    @action(detail=True, methods=["post"])
    def renew(self, request, pk=None):
        contract = self.get_object()
        new_expiry = request.data.get("new_expiry")
        invoice_id = request.data.get("invoice_id")
        if not new_expiry:
            return Response({"detail": "new_expiry required."}, status=status.HTTP_400_BAD_REQUEST)
        prev = contract.expiry_date
        contract.expiry_date = new_expiry
        from dateutil.relativedelta import relativedelta
        contract.renewal_due_date = new_expiry - relativedelta(days=30)
        contract.status = "active"
        contract.save()
        RenewalHistory.objects.create(
            license_contract=contract,
            previous_expiry=prev,
            new_expiry=new_expiry,
            invoice_id=invoice_id or None,
            renewed_by=request.user,
        )
        return Response(LicenseContractSerializer(contract).data)


class AllocationViewSet(viewsets.ModelViewSet):
    queryset = Allocation.objects.select_related("software_asset", "department", "user")
    serializer_class = AllocationSerializer
    permission_classes = [SLMPermission, CanEditAssets]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["software_asset", "department", "active_flag"]
    ordering = ["-allocated_on"]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset = SoftwareAsset.objects.get(pk=serializer.validated_data["software_asset"].id)
        used = asset.allocations.filter(active_flag=True).count()
        if used >= asset.total_licenses:
            return Response(
                {"detail": "No available licenses. Over-allocation not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [SLMPermission, CanEditFinance]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["company_name", "contact_person", "email"]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related("vendor", "license_contract", "created_by").prefetch_related("payments")
    permission_classes = [SLMPermission, CanEditFinance]
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["vendor", "currency"]
    ordering = ["-invoice_date"]


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("user").order_by("-timestamp")
    serializer_class = AuditLogSerializer
    permission_classes = [SLMPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["entity", "change_type", "user"]


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [SLMPermission]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    def retrieve(self, request, *args, **kwargs):
        inst = self.get_object()
        inst.is_read = True
        inst.save(update_fields=["is_read"])
        return Response(NotificationSerializer(inst).data)

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return Response({"status": "ok"})


# Dashboard API views
class DashboardStatsViewSet(viewsets.ViewSet):
    permission_classes = [SLMPermission]

    def list(self, request):
        today = timezone.now().date()
        from datetime import timedelta
        next_30 = today + timedelta(days=30)
        next_90 = today + timedelta(days=90)
        assets = SoftwareAsset.objects.filter(is_deleted=False)
        contracts = LicenseContract.objects.all()
        active_contracts = contracts.filter(status="active")
        expiring_30 = active_contracts.filter(expiry_date__lte=next_30, expiry_date__gte=today)
        expiring_90 = active_contracts.filter(expiry_date__lte=next_90, expiry_date__gt=next_30)
        expired = contracts.filter(expiry_date__lt=today, status="active")
        total_spend = Invoice.objects.aggregate(s=Sum("total"))["s"] or 0
        return Response({
            "total_assets": assets.count(),
            "active_contracts": active_contracts.count(),
            "expiring_in_30_days": expiring_30.count(),
            "expiring_in_90_days": expiring_90.count(),
            "expired_pending": expired.count(),
            "total_spend": str(total_spend),
            "total_vendors": Vendor.objects.filter(is_active=True).count(),
        })
