from buys.views import SuppliersViewSet, BuyVoucherViewSet

from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'suppliers', SuppliersViewSet, basename="suppliers")
router.register(r'vouchers', BuyVoucherViewSet, basename="vouchers")

urlpatterns = [
    path("", include(router.urls))
]