from agents.views import AgentsViewSet

from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'agents', AgentsViewSet, basename="agents")

urlpatterns = [
    path("", include(router.urls))
]
