from rest_framework.permissions import BasePermission
from rest_framework.request import HttpRequest

from agents.constants import AGENT_ONLY_ALLOWED
from agents.models import Agent



class IsAdminOrAgent(BasePermission):
    
    message = AGENT_ONLY_ALLOWED
    
    def has_permission(self, request: HttpRequest, view):
                
        if request.user.__class__ == "AnonymousUser":
            return False
        
        if request.user.is_staff:
            return True
                
        try:
            Agent.objects.get(user=request.user)
            return True
        except Agent.DoesNotExist:
            return False