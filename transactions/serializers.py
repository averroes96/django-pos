from rest_framework.serializers import ModelSerializer

from transactions.models import ClientTransaction, Expense, SupplierTransaction

from django.db.transaction import atomic

from agents.models import Agent


class ClientTransactionSerializer(ModelSerializer):
    
    def validate(self, attrs):
        if self.instance: # it's an update (cannot change client)
            attrs.pop("client", None) # in case client was passed
        
        return super().validate(attrs)
    
    @atomic
    def create(self, validated_data):
        agent = Agent.objects.get(user=self.context.get("request").user)
        validated_data["agent"] = agent
        
        return super().create(validated_data)
    
    @atomic
    def update(self, instance, validated_data):
        agent = Agent.objects.get(user=self.context.get("request").user)
        validated_data["agent"] = agent
        
        return super().update(instance, validated_data)
    
    class Meta:
        model = ClientTransaction
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "agent"]


class SupplierTransactionSerializer(ModelSerializer):
    
    def validate(self, attrs):
        if self.instance: # it's an update (cannot change supplier)
            attrs.pop("supplier", None) # in case supplier was passed
        
        return super().validate(attrs)
    
    @atomic
    def create(self, validated_data):
        agent = Agent.objects.get(user=self.context.get("request").user)
        validated_data["agent"] = agent
        
        return super().create(validated_data)

    @atomic
    def update(self, instance, validated_data):
        agent = Agent.objects.get(user=self.context.get("request").user)
        validated_data["agent"] = agent
        
        return super().update(instance, validated_data)
    
    class Meta:
        model = SupplierTransaction
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "agent"]


class ExpenseSerializer(ModelSerializer):
    
    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]