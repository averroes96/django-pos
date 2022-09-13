from django.contrib.auth.models import Permission

from rest_framework.permissions import BasePermission
from rest_framework.request import HttpRequest

from agents.constants import AGENT_ONLY_ALLOWED
from agents.models import Agent



class IsAgent(BasePermission):
    
    message = AGENT_ONLY_ALLOWED
    
    def has_permission(self, request: HttpRequest, view):
        try:
            Agent.objects.get(user=request.user)
            return True
        except Agent.DoesNotExist:
            return False