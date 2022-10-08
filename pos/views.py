from rest_framework.viewsets import ModelViewSet

from pos.models import SaleVoucher
from pos.serializers import(
    SaleVoucherListSerializer,
    SaleVoucherCreateSerializer,
    SaleVoucherRetrieveSerializer,
)

from sells.permissions import SellsPermission

# Create your views here.


class SaleVoucherViewSet(ModelViewSet):
    
    permission_classes = [SellsPermission]
    
    def get_serializer_class(self):
        if self.action == "create":
            return SaleVoucherCreateSerializer
        elif self.action == "list":
            return SaleVoucherListSerializer
        else:
            return SaleVoucherRetrieveSerializer
    
    def get_queryset(self):
        return SaleVoucher.objects.all()
