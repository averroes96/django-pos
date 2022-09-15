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
    
    def get_queryset(self):
        return ClientTransaction.objects.all()
    
    @atomic
    def create(self, request: HttpRequest, *args, **kwargs):
        agent = Agent.objects.get(user=request.user)
        request.data.update({"agent" : agent.id})
        
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'value': openapi.Schema(type=openapi.TYPE_INTEGER, description=0),
        }
    ))
    @atomic
    def partial_update(self, request, *args, **kwargs):
        agent = Agent.objects.get(user=request.user)
        request.data.update({"agent" : agent.id})
        
        return super().partial_update(request, *args, **kwargs)


class SupplierTransactionViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = SupplierTransactionSerializer
    
    def get_queryset(self):
        return SupplierTransaction.objects.all()
    
    @atomic
    def create(self, request: HttpRequest, *args, **kwargs):
        agent = get_object_or_404(Agent, user=request.user)
        request.data.update({"agent" : agent})
        
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'value': openapi.Schema(type=openapi.TYPE_INTEGER, description=0),
        }
    ))
    @atomic
    def partial_update(self, request, *args, **kwargs):
        agent = Agent.objects.get(user=request.user)
        request.data.update({"agent" : agent.id})
        
        return super().partial_update(request, *args, **kwargs)


class ExpenseViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ExpenseSerializer
    
    def get_queryset(self):
        return Expense.objects.all()

    @atomic
    def create(self, request: HttpRequest, *args, **kwargs):
        agent = get_object_or_404(Agent, user=request.user)
        request.data.update({"agent" : agent.id})
        
        return super().create(request, *args, **kwargs)
    
    @atomic
    def partial_update(self, request, *args, **kwargs):
        agent = Agent.objects.get(user=request.user)
        request.data.update({"agent" : agent.id})
        
        return super().partial_update(request, *args, **kwargs)