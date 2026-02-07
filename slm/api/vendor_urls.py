from django.urls import path, include
from rest_framework.routers import DefaultRouter
from slm.api.views import VendorViewSet

router = DefaultRouter()
router.register("", VendorViewSet, basename="vendor")
urlpatterns = [path("", include(router.urls))]
