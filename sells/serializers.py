from rest_framework.serializers import ModelSerializer, CharField

from sells.models import Client



class ClientSerializer(ModelSerializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    
    class Meta:
        model = Client
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
        read_only_fields = ["id", "balance_initial", "created_at", "updated_at"]