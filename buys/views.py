from rest_framework.viewsets import ModelViewSet

from buys.models import Supplier, BuyVoucher
from buys.serializers import (
    SupplierSerializer, 
    BuyVoucherListSerializer, 
    BuyVoucherCreateSerializer,
    BuyVoucherRetrieveSerializer
)
from buys.permissions import BuysPermission

# Create your views here.


class SuppliersViewSet(ModelViewSet):
    
    serializer_class = SupplierSerializer
    permission_classes = [BuysPermission]
    
    def get_queryset(self):
        return Supplier.objects.all()


class BuyVoucherViewSet(ModelViewSet):
    
    permission_classes = [BuysPermission]
    
    def get_serializer_class(self):
        if self.action == "create":
            return BuyVoucherCreateSerializer
        elif self.action == "list":
            return BuyVoucherListSerializer
        else:
            return BuyVoucherRetrieveSerializer
    
    def get_queryset(self):
        return BuyVoucher.objects.all()