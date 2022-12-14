from rest_framework.permissions import BasePermission
from rest_framework.request import HttpRequest

from buys.constants import BUY_PERMISSION_MESSAGE

from agents.models import Agent


class BuysPermission(BasePermission):
    message = BUY_PERMISSION_MESSAGE

    def has_permission(self, request: HttpRequest, view):
        """
        > If the user has the permission to buy, then return True. Otherwise, return False
        
        :param request: The incoming request
        :type request: HttpRequest
        :param view: The view that the permission is being checked against
        :return: A boolean value.
        """
        buy_permission_codename = f"agents.{Agent.Permission.BUYS_PERMISSION_CODENAME}"
        
        if request.user.has_perm(buy_permission_codename):
                return True
        else:
            return False