from sells.views import ClientsViewSet, SellVoucherViewSet

from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clients', ClientsViewSet, basename="clients")
router.register(r'vouchers', SellVoucherViewSet, basename="vouchers")

urlpatterns = [
    path("", include(router.urls))
]