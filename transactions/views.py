from rest_framework.viewsets import ModelViewSet

from transactions.serializers import (
    ClientTransactionSerializer, 
    ExpenseSerializer, 
    SupplierTransactionSerializer
)
from transactions.models import SupplierTransaction, ClientTransaction, Expense

from agents.permissions import IsAdminOrAgent


# Create your views here.


class ClientTransactionViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ClientTransactionSerializer
    
    def get_queryset(self):
        return ClientTransaction.objects.all()


class SupplierTransactionViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = SupplierTransactionSerializer
    
    def get_queryset(self):
        return SupplierTransaction.objects.all()


class ExpenseViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ExpenseSerializer
    
    def get_queryset(self):
        return Expense.objects.all()