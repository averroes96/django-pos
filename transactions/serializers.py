from rest_framework.serializers import ModelSerializer, UUIDField

from transactions.models import ClientTransaction, Expense, SupplierTransaction

from django.db.transaction import atomic


class ClientTransactionSerializer(ModelSerializer):
    
    @atomic
    def update(self, instance, validated_data):
        validated_data.pop("client") # in case supplier was passed
        return super().update(instance, validated_data)
    
    class Meta:
        model = ClientTransaction
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class SupplierTransactionSerializer(ModelSerializer):

    @atomic
    def update(self, instance, validated_data):
        validated_data.pop("supplier") # in case supplier was passed
        return super().update(instance, validated_data)
    
    class Meta:
        model = SupplierTransaction
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ExpenseSerializer(ModelSerializer):
    
    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]