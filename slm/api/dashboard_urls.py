from django.urls import path
from rest_framework.routers import DefaultRouter
from slm.api.views import DashboardStatsViewSet

router = DefaultRouter()
router.register("stats", DashboardStatsViewSet, basename="dashboard-stats")
urlpatterns = router.urls
