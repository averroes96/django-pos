from rest_framework.viewsets import ModelViewSet

from sells.models import Client, SellVoucher
from sells.serializers import (
    ClientSerializer, 
    SellVoucherListSerializer, 
    SellVoucherRetrieveSerializer,
    SellVoucherCreateSerializer
)
from sells.permissions import SellsPermission

# Create your views here.

class ClientsViewSet(ModelViewSet):
    
    serializer_class = ClientSerializer
    permission_classes = [SellsPermission]
    throttle_scope = "sells"
    
    def get_queryset(self):
        return Client.objects.all()


class SellVoucherViewSet(ModelViewSet):
    
    permission_classes = [SellsPermission]
    throttle_scope = "sells"
    
    def get_serializer_class(self):
        if self.action == "create":
            return SellVoucherCreateSerializer
        elif self.action == "list":
            return SellVoucherListSerializer
        else:
            return SellVoucherRetrieveSerializer
    
    def get_queryset(self):
        return SellVoucher.objects.all()
