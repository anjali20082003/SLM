from django.urls import path, include
from rest_framework.routers import DefaultRouter
from slm.api.views import AllocationViewSet

router = DefaultRouter()
router.register("", AllocationViewSet, basename="allocation")
urlpatterns = [path("", include(router.urls))]
