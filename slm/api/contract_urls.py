from django.urls import path, include
from rest_framework.routers import DefaultRouter
from slm.api.views import LicenseContractViewSet

router = DefaultRouter()
router.register("", LicenseContractViewSet, basename="contract")
urlpatterns = [path("", include(router.urls))]
