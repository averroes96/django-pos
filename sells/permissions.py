from django.contrib.auth.models import Permission

from rest_framework.permissions import BasePermission
from rest_framework.request import HttpRequest

from sells.constants import SELL_PERMISSION_MESSAGE

from agents.models import Agent


class SellsPermission(BasePermission):
    message = SELL_PERMISSION_MESSAGE

    def has_permission(self, request: HttpRequest, view):
        """
        > If the user has the permission to sell, then return True. Otherwise, return False
        
        :param request: The incoming request
        :type request: HttpRequest
        :param view: The view that the permission is being checked against
        :return: True or False
        """
        user = request.user
        
        if user.has_perm(f"agents.{Agent.Permission.SELLS_PERMISSION_CODENAME}"):
            return True
        
        return False