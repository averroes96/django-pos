from rest_framework.serializers import ModelSerializer, CharField

from buys.models import Supplier



class SupplierSerializer(ModelSerializer):
    
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    
    class Meta:
        model = Supplier
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_first",
            "phone_second",
            "fax",
            "fiscal_id",
            "trade_registry",
            "balance",
            "balance_initial",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "balance", "created_at", "updated_at"]