"""Template-based views for SLM web UI."""
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, FormView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import timedelta

from .models import (
    SoftwareAsset, LicenseContract, Allocation, Vendor, Invoice, Payment,
    Notification, Department, Branch, AuditLog, RenewalHistory,
)
from .forms import (
    SoftwareAssetForm, LicenseContractForm, VendorForm,
    AllocationForm, InvoiceForm, PaymentForm, DepartmentForm, BranchForm,
)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "slm/dashboard.html"
    context_object_name = "stats"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        next_30 = today + timedelta(days=30)
        next_90 = today + timedelta(days=90)
        assets = SoftwareAsset.objects.filter(is_deleted=False)
        contracts = LicenseContract.objects.all()
        active = contracts.filter(status="active")
        expiring_30 = active.filter(expiry_date__lte=next_30, expiry_date__gte=today)
        expiring_90 = active.filter(expiry_date__lte=next_90, expiry_date__gt=next_30)
        expired = contracts.filter(expiry_date__lt=today, status="active")
        total_spend = Invoice.objects.aggregate(s=Sum("total"))["s"] or 0
        ctx["total_assets"] = assets.count()
        ctx["active_contracts"] = active.count()
        ctx["expiring_in_30"] = expiring_30.count()
        ctx["expiring_in_90"] = expiring_90.count()
        ctx["expired_pending"] = expired.count()
        ctx["total_spend"] = total_spend
        ctx["total_vendors"] = Vendor.objects.filter(is_active=True).count()
        ctx["expiring_contracts"] = expiring_30.select_related("software_asset", "vendor")[:10]
        ctx["unread_notifications"] = Notification.objects.filter(user=user, is_read=False).count()
        return ctx


class AssetListView(LoginRequiredMixin, ListView):
    model = SoftwareAsset
    template_name = "slm/asset_list.html"
    context_object_name = "assets"
    paginate_by = 20

    def get_queryset(self):
        qs = SoftwareAsset.objects.filter(is_deleted=False).select_related("created_by").order_by("name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(description__icontains=q) | Q(tags__icontains=q) | Q(category__icontains=q)
            )
        cat = self.request.GET.get("category")
        if cat:
            qs = qs.filter(category=cat)
        return qs


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = SoftwareAsset
    template_name = "slm/asset_detail.html"
    context_object_name = "asset"

    def get_queryset(self):
        return SoftwareAsset.objects.filter(is_deleted=False).prefetch_related("contracts", "allocations")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["allocations_active"] = self.object.allocations.filter(active_flag=True).select_related("department", "user")
        return ctx


class AssetCreateView(LoginRequiredMixin, CreateView):
    model = SoftwareAsset
    form_class = SoftwareAssetForm
    template_name = "slm/asset_form.html"
    success_url = reverse_lazy("slm:asset_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.is_deleted = False
        messages.success(self.request, "Software asset created successfully.")
        return super().form_valid(form)


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = SoftwareAsset
    form_class = SoftwareAssetForm
    template_name = "slm/asset_form.html"
    context_object_name = "asset"
    success_url = reverse_lazy("slm:asset_list")

    def get_queryset(self):
        return SoftwareAsset.objects.filter(is_deleted=False)

    def form_valid(self, form):
        messages.success(self.request, "Software asset updated successfully.")
        return super().form_valid(form)


class ContractListView(LoginRequiredMixin, ListView):
    model = LicenseContract
    template_name = "slm/contract_list.html"
    context_object_name = "contracts"
    paginate_by = 20

    def get_queryset(self):
        qs = LicenseContract.objects.select_related("software_asset", "vendor").order_by("-expiry_date")
        status_filter = self.request.GET.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs


class ContractDetailView(LoginRequiredMixin, DetailView):
    model = LicenseContract
    template_name = "slm/contract_detail.html"
    context_object_name = "contract"

    def get_queryset(self):
        return LicenseContract.objects.select_related("software_asset", "vendor").prefetch_related("invoices", "renewal_history")


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = LicenseContract
    form_class = LicenseContractForm
    template_name = "slm/contract_form.html"
    success_url = reverse_lazy("slm:contract_list")

    def form_valid(self, form):
        messages.success(self.request, "License contract created successfully.")
        return super().form_valid(form)


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    model = LicenseContract
    form_class = LicenseContractForm
    template_name = "slm/contract_form.html"
    context_object_name = "contract"
    success_url = reverse_lazy("slm:contract_list")

    def form_valid(self, form):
        messages.success(self.request, "License contract updated successfully.")
        return super().form_valid(form)


class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = "slm/vendor_list.html"
    context_object_name = "vendors"
    paginate_by = 20

    def get_queryset(self):
        qs = Vendor.objects.order_by("company_name")
        if self.request.GET.get("active") == "1":
            qs = qs.filter(is_active=True)
        return qs


class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = "slm/vendor_form.html"
    success_url = reverse_lazy("slm:vendor_list")

    def form_valid(self, form):
        messages.success(self.request, "Vendor created successfully.")
        return super().form_valid(form)


class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = "slm/vendor_form.html"
    context_object_name = "vendor"
    success_url = reverse_lazy("slm:vendor_list")

    def get_queryset(self):
        return Vendor.objects.all()

    def form_valid(self, form):
        messages.success(self.request, "Vendor updated successfully.")
        return super().form_valid(form)


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "slm/invoice_list.html"
    context_object_name = "invoices"
    paginate_by = 20

    def get_queryset(self):
        return Invoice.objects.select_related("vendor", "license_contract", "created_by").order_by("-invoice_date")


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "slm/invoice_detail.html"
    context_object_name = "invoice"

    def get_queryset(self):
        return Invoice.objects.select_related("vendor", "license_contract").prefetch_related("payments")


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "slm/invoice_form.html"
    success_url = reverse_lazy("slm:invoice_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Invoice created successfully.")
        return super().form_valid(form)


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "slm/invoice_form.html"
    context_object_name = "invoice"
    success_url = reverse_lazy("slm:invoice_list")

    def form_valid(self, form):
        messages.success(self.request, "Invoice updated successfully.")
        return super().form_valid(form)


class AllocationListView(LoginRequiredMixin, ListView):
    model = Allocation
    template_name = "slm/allocation_list.html"
    context_object_name = "allocations"
    paginate_by = 20

    def get_queryset(self):
        return Allocation.objects.select_related("software_asset", "department", "user").order_by("-allocated_on")


class AllocationCreateView(LoginRequiredMixin, CreateView):
    model = Allocation
    form_class = AllocationForm
    template_name = "slm/allocation_form.html"
    success_url = reverse_lazy("slm:allocation_list")

    def get_initial(self):
        initial = super().get_initial()
        asset_id = self.request.GET.get("asset")
        if asset_id:
            try:
                initial["software_asset"] = SoftwareAsset.objects.filter(is_deleted=False).get(pk=asset_id).pk
            except (SoftwareAsset.DoesNotExist, ValueError):
                pass
        return initial

    def form_valid(self, form):
        asset = form.cleaned_data["software_asset"]
        used = asset.allocations.filter(active_flag=True).count()
        if used >= asset.total_licenses:
            form.add_error("software_asset", "No available licenses for this asset.")
            return self.form_invalid(form)
        messages.success(self.request, "Allocation created successfully.")
        return super().form_valid(form)


class AllocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Allocation
    form_class = AllocationForm
    template_name = "slm/allocation_form.html"
    context_object_name = "allocation"
    success_url = reverse_lazy("slm:allocation_list")

    def form_valid(self, form):
        if form.cleaned_data.get("returned_on"):
            form.instance.active_flag = False
        messages.success(self.request, "Allocation updated successfully.")
        return super().form_valid(form)


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "slm/payment_form.html"

    def get_initial(self):
        initial = super().get_initial()
        invoice_id = self.request.GET.get("invoice") or self.kwargs.get("invoice_id")
        if invoice_id:
            try:
                initial["invoice"] = Invoice.objects.get(pk=invoice_id).pk
            except (Invoice.DoesNotExist, ValueError):
                pass
        return initial

    def get_success_url(self):
        inv = self.object.invoice
        return reverse_lazy("slm:invoice_detail", kwargs={"pk": inv.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Payment recorded successfully.")
        return super().form_valid(form)


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "slm/payment_form.html"
    context_object_name = "payment"

    def get_success_url(self):
        return reverse_lazy("slm:invoice_detail", kwargs={"pk": self.object.invoice_id})

    def form_valid(self, form):
        messages.success(self.request, "Payment updated successfully.")
        return super().form_valid(form)


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "slm/department_list.html"
    context_object_name = "departments"
    paginate_by = 20

    def get_queryset(self):
        return Department.objects.select_related("branch").order_by("name")


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "slm/department_form.html"
    success_url = reverse_lazy("slm:department_list")

    def form_valid(self, form):
        messages.success(self.request, "Department created successfully.")
        return super().form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "slm/department_form.html"
    context_object_name = "department"
    success_url = reverse_lazy("slm:department_list")

    def form_valid(self, form):
        messages.success(self.request, "Department updated successfully.")
        return super().form_valid(form)


class BranchListView(LoginRequiredMixin, ListView):
    model = Branch
    template_name = "slm/branch_list.html"
    context_object_name = "branches"
    paginate_by = 20

    def get_queryset(self):
        qs = Branch.objects.order_by("name")
        if self.request.GET.get("active") == "1":
            qs = qs.filter(is_active=True)
        return qs


class BranchCreateView(LoginRequiredMixin, CreateView):
    model = Branch
    form_class = BranchForm
    template_name = "slm/branch_form.html"
    success_url = reverse_lazy("slm:branch_list")

    def form_valid(self, form):
        messages.success(self.request, "Branch created successfully.")
        return super().form_valid(form)


class BranchUpdateView(LoginRequiredMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = "slm/branch_form.html"
    context_object_name = "branch"
    success_url = reverse_lazy("slm:branch_list")

    def get_queryset(self):
        return Branch.objects.all()

    def form_valid(self, form):
        messages.success(self.request, "Branch updated successfully.")
        return super().form_valid(form)


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "slm/reports.html"


class ReportInventoryView(LoginRequiredMixin, TemplateView):
    template_name = "slm/report_inventory.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["assets"] = SoftwareAsset.objects.filter(is_deleted=False).select_related("created_by").order_by("name")
        return ctx


class ReportRenewalView(LoginRequiredMixin, TemplateView):
    template_name = "slm/report_renewal.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.now().date()
        end = today + timedelta(days=365)
        ctx["contracts"] = LicenseContract.objects.filter(
            expiry_date__gte=today, expiry_date__lte=end
        ).select_related("software_asset", "vendor").order_by("expiry_date")
        return ctx


class ReportVendorSpendView(LoginRequiredMixin, TemplateView):
    template_name = "slm/report_vendor_spend.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from django.db.models import Sum
        spend = Invoice.objects.values("vendor").annotate(total=Sum("total")).order_by("-total")
        vendor_ids = [s["vendor"] for s in spend if s["vendor"]]
        vendors = {v.id: v for v in Vendor.objects.filter(id__in=vendor_ids)}
        ctx["rows"] = [
            {"vendor": vendors.get(s["vendor"]), "total": s["total"]} for s in spend
        ]
        return ctx


class ReportAuditView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = "slm/report_audit.html"
    context_object_name = "logs"
    paginate_by = 50

    def get_queryset(self):
        return AuditLog.objects.select_related("user").order_by("-timestamp")


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "slm/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")


class NotificationMarkReadView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=kwargs["pk"], user=request.user)
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        messages.success(request, "Notification marked as read.")
        return redirect(request.GET.get("next", "slm:notification_list"))


class NotificationMarkAllReadView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        Notification.objects.filter(user=request.user).update(is_read=True)
        messages.success(request, "All notifications marked as read.")
        return redirect("slm:notification_list")


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = SoftwareAsset
    template_name = "slm/confirm_delete.html"
    success_url = reverse_lazy("slm:asset_list")

    def get_queryset(self):
        return SoftwareAsset.objects.filter(is_deleted=False)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Perform soft delete
        self.object.is_deleted = True
        self.object.save()
        messages.success(request, "Software asset deleted successfully.")
        return redirect(self.success_url)


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    model = LicenseContract
    template_name = "slm/confirm_delete.html"
    success_url = reverse_lazy("slm:contract_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, "License contract deleted successfully.")
        return redirect(self.success_url)


class VendorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendor
    template_name = "slm/confirm_delete.html"
    success_url = reverse_lazy("slm:vendor_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Deactivate instead of hard delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, "Vendor deactivated successfully.")
        return redirect(self.success_url)


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = "slm/confirm_delete.html"
    success_url = reverse_lazy("slm:invoice_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, "Invoice deleted successfully.")
        return redirect(self.success_url)


class AllocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Allocation
    template_name = "slm/confirm_delete.html"
    success_url = reverse_lazy("slm:allocation_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Deactivate instead of hard delete
        self.object.active_flag = False
        self.object.save()
        messages.success(request, "Allocation deactivated successfully.")
        return redirect(self.success_url)


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = "slm/confirm_delete.html"
    success_url = reverse_lazy("slm:department_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Deactivate instead of hard delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, "Department deactivated successfully.")
        return redirect(self.success_url)


class BranchDeleteView(LoginRequiredMixin, DeleteView):
    model = Branch
    template_name = "slm/confirm_delete.html"
    success_url = reverse_lazy("slm:branch_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Deactivate instead of hard delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, "Branch deactivated successfully.")
        return redirect(self.success_url)
