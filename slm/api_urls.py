"""REST API URLs for SLM."""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("assets/", include("slm.api.asset_urls")),
    path("contracts/", include("slm.api.contract_urls")),
    path("allocations/", include("slm.api.allocation_urls")),
    path("vendors/", include("slm.api.vendor_urls")),
    path("invoices/", include("slm.api.invoice_urls")),
    path("dashboard/", include("slm.api.dashboard_urls")),
    path("reports/", include("slm.api.report_urls")),
    path("audit/", include("slm.api.audit_urls")),
    path("notifications/", include("slm.api.notification_urls")),
]
