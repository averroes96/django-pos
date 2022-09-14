from django.urls import path, include

from rest_framework.routers import DefaultRouter

from transactions.views import ClientTransactionViewSet, ExpenseViewSet, SupplierTransactionViewSet



router = DefaultRouter()
router.register(r'clients', ClientTransactionViewSet, basename="clients")
router.register(r'suppliers', SupplierTransactionViewSet, basename="suppliers")
router.register(r'expenses', ExpenseViewSet, basename="expenses")

urlpatterns = [
    path("", include(router.urls))
]