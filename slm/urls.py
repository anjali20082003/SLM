"""Web (template) URLs for SLM."""
from django.urls import path
from . import views

app_name = "slm"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    # Assets
    path("assets/", views.AssetListView.as_view(), name="asset_list"),
    path("assets/add/", views.AssetCreateView.as_view(), name="asset_add"),
    path("assets/<int:pk>/", views.AssetDetailView.as_view(), name="asset_detail"),
    path("assets/<int:pk>/edit/", views.AssetUpdateView.as_view(), name="asset_edit"),
    path("assets/<int:pk>/delete/", views.AssetDeleteView.as_view(), name="asset_delete"),
    # Contracts
    path("contracts/", views.ContractListView.as_view(), name="contract_list"),
    path("contracts/add/", views.ContractCreateView.as_view(), name="contract_add"),
    path("contracts/<int:pk>/", views.ContractDetailView.as_view(), name="contract_detail"),
    path("contracts/<int:pk>/edit/", views.ContractUpdateView.as_view(), name="contract_edit"),
    path("contracts/<int:pk>/delete/", views.ContractDeleteView.as_view(), name="contract_delete"),
    # Vendors
    path("vendors/", views.VendorListView.as_view(), name="vendor_list"),
    path("vendors/add/", views.VendorCreateView.as_view(), name="vendor_add"),
    path("vendors/<int:pk>/edit/", views.VendorUpdateView.as_view(), name="vendor_edit"),
    path("vendors/<int:pk>/delete/", views.VendorDeleteView.as_view(), name="vendor_delete"),
    # Invoices
    path("invoices/", views.InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/add/", views.InvoiceCreateView.as_view(), name="invoice_add"),
    path("invoices/<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
    path("invoices/<int:pk>/edit/", views.InvoiceUpdateView.as_view(), name="invoice_edit"),
    path("invoices/<int:pk>/delete/", views.InvoiceDeleteView.as_view(), name="invoice_delete"),
    path("invoices/<int:invoice_id>/payments/add/", views.PaymentCreateView.as_view(), name="payment_add"),
    path("payments/<int:pk>/edit/", views.PaymentUpdateView.as_view(), name="payment_edit"),
    # Allocations
    path("allocations/", views.AllocationListView.as_view(), name="allocation_list"),
    path("allocations/add/", views.AllocationCreateView.as_view(), name="allocation_add"),
    path("allocations/<int:pk>/edit/", views.AllocationUpdateView.as_view(), name="allocation_edit"),
    path("allocations/<int:pk>/delete/", views.AllocationDeleteView.as_view(), name="allocation_delete"),
    # Departments
    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path("departments/add/", views.DepartmentCreateView.as_view(), name="department_add"),
    path("departments/<int:pk>/edit/", views.DepartmentUpdateView.as_view(), name="department_edit"),
    path("departments/<int:pk>/delete/", views.DepartmentDeleteView.as_view(), name="department_delete"),
    # Branches
    path("branches/", views.BranchListView.as_view(), name="branch_list"),
    path("branches/add/", views.BranchCreateView.as_view(), name="branch_add"),
    path("branches/<int:pk>/edit/", views.BranchUpdateView.as_view(), name="branch_edit"),
    path("branches/<int:pk>/delete/", views.BranchDeleteView.as_view(), name="branch_delete"),
    # Reports & Notifications
    path("reports/", views.ReportsView.as_view(), name="reports"),
    path("reports/inventory/", views.ReportInventoryView.as_view(), name="report_inventory"),
    path("reports/renewal/", views.ReportRenewalView.as_view(), name="report_renewal"),
    path("reports/vendor-spend/", views.ReportVendorSpendView.as_view(), name="report_vendor_spend"),
    path("reports/audit/", views.ReportAuditView.as_view(), name="report_audit"),
    path("notifications/", views.NotificationListView.as_view(), name="notification_list"),
    path("notifications/<int:pk>/read/", views.NotificationMarkReadView.as_view(), name="notification_mark_read"),
    path("notifications/mark-all-read/", views.NotificationMarkAllReadView.as_view(), name="notification_mark_all_read"),
]
