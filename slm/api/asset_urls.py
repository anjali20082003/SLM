from django.urls import path, include
from rest_framework.routers import DefaultRouter
from slm.api.views import SoftwareAssetViewSet

router = DefaultRouter()
router.register("", SoftwareAssetViewSet, basename="asset")
urlpatterns = [path("", include(router.urls))]
