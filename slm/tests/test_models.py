"""Tests for SLM models."""
import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from slm.models import Department, SoftwareAsset, Allocation, LicenseContract, Vendor

User = get_user_model()


@pytest.mark.django_db
def test_software_asset_licenses():
    dept = Department.objects.create(name="IT", code="IT")
    user = User.objects.create_user(email="u@test.com", password="pass", role="it_staff")
    asset = SoftwareAsset.objects.create(
        name="Test App", total_licenses=5, license_type="user", created_by=user
    )
    assert asset.used_licenses == 0
    assert asset.available_licenses == 5
    Allocation.objects.create(
        software_asset=asset, department=dept, user=user, active_flag=True
    )
    asset.refresh_from_db()
    assert asset.used_licenses == 1
    assert asset.available_licenses == 4


@pytest.mark.django_db
def test_license_contract_expiry():
    from datetime import date
    asset = SoftwareAsset.objects.create(name="App", total_licenses=1, license_type="user")
    vendor = Vendor.objects.create(company_name="Vendor Co")
    contract = LicenseContract.objects.create(
        software_asset=asset, vendor=vendor,
        purchase_date=date(2024, 1, 1), duration_months=12
    )
    assert contract.expiry_date == date(2025, 1, 1)
