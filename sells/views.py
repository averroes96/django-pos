from rest_framework.viewsets import ModelViewSet

from sells.models import Client
from sells.serializers import ClientSerializer
from sells.permissions import SellsPermission

# Create your views here.

class ClientsViewSet(ModelViewSet):
    
    serializer_class = ClientSerializer
    permission_classes = [SellsPermission]
    
    def get_queryset(self):
        return Client.objects.all()
