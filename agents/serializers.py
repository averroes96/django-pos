from django.contrib.auth.models import User, Permission
from django.db.transaction import atomic

from rest_framework.serializers import ModelSerializer, CharField, ListField

from agents.models import Agent



class AgentSerializer(ModelSerializer):
    
    username = CharField(source="user.username")
    password = CharField(source="user.password", write_only=True)
    email = CharField(source="user.email", required=False)
    last_login = CharField(source="user.email", required=False)
    token = CharField(source="user.auth_token.key", required=False)
    permissions = ListField(source="user.user_permissions.all", required=False)
    
    @atomic
    def create(self, validated_data):
        # Direct assignment to the forward side of a many-to-many set is prohibited. 
        # Use user_permissions.set() instead.
        permissions_list = validated_data.get("user").pop("user_permissions")
        
        # create agent's user
        user = User.objects.create(**validated_data.get("user"))
        
        # set user permissions
        permissions_all = permissions_list.get("all")
        
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