from django.contrib.auth.models import User, Permission
from django.db.transaction import atomic
from django.db import DatabaseError

from rest_framework.serializers import (
    ModelSerializer, 
    CharField, 
    ListField, 
    ValidationError,
    RegexField,
)

from agents.models import Agent
from agents.constants import USER_DATABASE_ERROR



class AgentSerializer(ModelSerializer):
    
    phone = RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    
    username = CharField(source="user.username")
    password = CharField(source="user.password", write_only=True)
    email = CharField(source="user.email", required=False)
    last_login = CharField(source="user.email", required=False)
    token = CharField(source="user.auth_token.key", required=False)
    permissions = ListField(source="user.user_permissions.values", required=False)
    
    @atomic
    def create(self, validated_data):
        # Direct assignment to the forward side of a many-to-many set is prohibited. 
        # Use user_permissions.set() instead.
        permissions_list = validated_data.get("user").pop("user_permissions", None)
        
        # create agent's user
        try:
            user = User.objects.create(**validated_data.get("user"))
        except DatabaseError:
            raise ValidationError({"detail": USER_DATABASE_ERROR})
        
        # set user permissions
        if permissions_list:
            permissions_all = permissions_list.get("values")
            
            if permissions_list:
                permissions = Permission.objects.filter(
                    codename__in=permissions_all
                )
                if permissions: user.user_permissions.set(permissions)
        
        # create agent
        agent = Agent(phone=validated_data.get("phone"), address=validated_data.get("address"), user=user)
        if validated_data.get("is_admin"): agent.is_admin = validated_data.get("is_admin")
        agent.save()
        
        return agent
    
    
    @atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    class Meta:
        model = Agent
        fields = [
            "id",
            "username",
            "password",
            "email",
            "phone",
            "address",
            "is_admin",
            "created_at",
            "updated_at",
            "last_login",
            "token",
            "permissions"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_login", "token"]