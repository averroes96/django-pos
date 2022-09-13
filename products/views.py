from rest_framework.viewsets import ModelViewSet

from products.models import Product, ProductFamily, Unit
from products.serializers import ProductFamilySerializer, ProductSerializer, UnitSerializer

from agents.permissions import IsAgent

# Create your views here.


class ProductFamilyViewSet(ModelViewSet):
    
    permission_classes = [IsAgent]
    serializer_class = [ProductFamilySerializer]

class UnitViewSet(ModelViewSet):
    
    permission_classes = [IsAgent]
    serializer_class = [UnitSerializer]


class ProductViewSet(ModelViewSet):
    
    permission_classes = [IsAgent]
    serializer_class = [ProductSerializer]