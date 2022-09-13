from django.contrib.auth.models import Permission
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.request import HttpRequest

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from agents.models import Agent
from agents.serializers import AgentSerializer
from agents.constants import AGENT_LOGGED_OUT

# Create your views here.

class AgentsViewSet(ModelViewSet):
    
    serializer_class = AgentSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Agent.objects.all()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'login':
            permission_classes = [AllowAny]
        elif self.action == 'logout':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]
    
    
    @action(detail=False, methods=["GET"])
    def permissions(self, request: HttpRequest):
        
        perms = Permission.objects.filter(
            codename__in=Agent.AGENT_CUSTOM_PERMISSIONS
        ).values("codename", "name")
        
        return Response(data={"permissions" : perms})
    
    
    @action(detail=False, methods=["POST"])
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def login(self, request: HttpRequest):
        
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        
        agent = get_object_or_404(klass=Agent, user__username=username, user__password=password)
        login(request, agent.user)
        
        return Response(self.serializer_class(instance=agent).data)
    
    
    @action(detail=False, methods=["POST"])
    @swagger_auto_schema(responses={200: AGENT_LOGGED_OUT})
    def logout(self, request: HttpRequest):

        logout(request)
        return Response({"detail": AGENT_LOGGED_OUT})