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
        user = request.user
        buy_permission_codename = f"agents.{Agent.Permission.BUYS_PERMISSION_CODENAME}"
        buy_with_debt_permission_codename = f"agents.{Agent.Permission.BUYS_DEBT_PERMISSION_CODENAME}"
        
        print(view.action)
        
        if view.action in ["create", "update", "partial_update"]: # check permissions
            if (
                user.has_perm(buy_permission_codename) and
                user.has_perm(buy_with_debt_permission_codename)
            ): # check user is an agent
                try:
                    Agent.objects.get(user=user)
                    return True
                except Agent.DoesNotExist:
                    return False
        elif user.has_perm(buy_permission_codename):
                return True
        else:
            return False