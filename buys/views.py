from rest_framework.viewsets import ModelViewSet

from buys.models import Supplier
from buys.serializers import SupplierSerializer
from buys.permissions import BuysPermission

# Create your views here.


class SuppliersViewSet(ModelViewSet):
    
    serializer_class = SupplierSerializer
    permission_classes = [BuysPermission]
    
    def get_queryset(self):
        return Supplier.objects.all()