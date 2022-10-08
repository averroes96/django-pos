from django.urls import path, include

from rest_framework.routers import DefaultRouter

from pos.views import SaleVoucherViewSet

router = DefaultRouter()
router.register(r'sales', SaleVoucherViewSet, basename="sales")

urlpatterns = [
    path("", include(router.urls))
]