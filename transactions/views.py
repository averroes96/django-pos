from rest_framework.viewsets import ModelViewSet
from rest_framework.request import HttpRequest

from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from transactions.serializers import (
    ClientTransactionSerializer, 
    ExpenseSerializer, 
    SupplierTransactionSerializer
)
from transactions.models import SupplierTransaction, ClientTransaction, Expense

from agents.permissions import IsAdminOrAgent
from agents.models import Agent


# Create your views here.


class ClientTransactionViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ClientTransactionSerializer
    throttle_scope = "transactions"
    
    def get_queryset(self):
        return ClientTransaction.objects.all()


class SupplierTransactionViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = SupplierTransactionSerializer
    throttle_scope = "transactions"
    
    def get_queryset(self):
        return SupplierTransaction.objects.all()


class ExpenseViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ExpenseSerializer
    throttle_scope = "transactions"
    
    def get_queryset(self):
        return Expense.objects.all()