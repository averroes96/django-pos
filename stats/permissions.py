from rest_framework.permissions import BasePermission
from rest_framework.request import HttpRequest

from stats.constants import STATS_PERMISSION_MESSAGE

from agents.models import Agent



class StatsPermission(BasePermission):
    
    message = STATS_PERMISSION_MESSAGE
    
    def has_permission(self, request: HttpRequest, view):
        user = request.user
        
        return user.has_perm(f"agents.{Agent.Permission.STATS_PERMISSION_CODENAME}")