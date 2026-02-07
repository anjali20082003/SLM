"""Tests for SLM API."""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from slm.models import SoftwareAsset, Vendor, Department

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    dept = Department.objects.create(name="IT", code="IT")
    return User.objects.create_user(
        email="api@test.com", password="testpass123", role="it_manager", department=dept
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
class TestAssetAPI:
    def test_list_assets_requires_auth(self, api_client):
        response = api_client.get("/api/assets/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_assets_authenticated(self, authenticated_client):
        response = authenticated_client.get("/api/assets/")
        assert response.status_code == status.HTTP_200_OK
        # Paginated response has "results" or list
        assert "results" in response.data or isinstance(response.data, list) or "count" in response.data

    def test_dashboard_stats(self, authenticated_client):
        response = authenticated_client.get("/api/dashboard/stats/")
        assert response.status_code == status.HTTP_200_OK
        assert "total_assets" in response.data
        assert "active_contracts" in response.data
