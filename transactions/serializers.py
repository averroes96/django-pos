from rest_framework.serializers import ModelSerializer

from transactions.models import ClientTransaction, Expense, SupplierTransaction



class ClientTransactionSerializer(ModelSerializer):
    
    class Meta:
        model = ClientTransaction
        fields = "__all__"


class SupplierTransactionSerializer(ModelSerializer):
    
    class Meta:
        model = SupplierTransaction
        fields = "__all__"


class ExpenseSerializer(ModelSerializer):
    
    class Meta:
        model = Expense
        fields = "__all__"