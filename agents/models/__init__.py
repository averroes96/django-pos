from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel


class Agent(BaseModel):
    
    class Permission:
        SELLS_PERMISSION_CODENAME = "sells_permissions"
        BUYS_PERMISSION_CODENAME = "buys_permissions"
        SELLS_DEBT_PERMISSION_CODENAME = "sells_debt_permission"
        BUYS_DEBT_PERMISSION_CODENAME = "buys_debt_permission"
        STATS_PERMISSION_CODENAME = "stats_permission"
    
    AGENT_CUSTOM_PERMISSIONS = [
        Permission.SELLS_PERMISSION_CODENAME,
        Permission.BUYS_PERMISSION_CODENAME,
        Permission.SELLS_DEBT_PERMISSION_CODENAME,
        Permission.BUYS_DEBT_PERMISSION_CODENAME,
        Permission.STATS_PERMISSION_CODENAME,
    ]
    
    phone = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    
    class Meta:
        get_latest_by = ["created_at"]
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.user.username}"