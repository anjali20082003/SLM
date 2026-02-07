from django.urls import path
from slm.api import report_views

urlpatterns = [
    path("inventory/", report_views.ReportInventoryView.as_view(), name="report-inventory"),
    path("renewal-calendar/", report_views.ReportRenewalCalendarView.as_view(), name="report-renewal-calendar"),
    path("vendor-spend/", report_views.ReportVendorSpendView.as_view(), name="report-vendor-spend"),
    path("audit-trail/", report_views.ReportAuditTrailView.as_view(), name="report-audit-trail"),
]
