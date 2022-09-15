from rest_framework.serializers import ModelSerializer, CharField

from buys.models import Supplier, BuyVoucher, BuyVoucherDetail



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
        read_only_fields = ["id", "balance_initial", "created_at", "updated_at"]


class BuyVoucherDetailCreateSerializer(ModelSerializer):
    
    class Meta:
        model = BuyVoucherDetail
        fields = ["article", "quantity", "price"]

class BuyVoucherListSerializer(ModelSerializer):
    
    class Meta:
        model = BuyVoucher
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class BuyVoucherCreateSerializer(ModelSerializer):
    
    details = BuyVoucherDetailCreateSerializer(many=True)
    
    def create(self, validated_data):
        
        details = validated_data.get("details")
        
        paid = validated_data.get("paid")
        with_debt = validated_data.get("with_debt", False)
        supplier = validated_data.get("supplier")
        number = validated_data.get("number")
        total = sum([detail.get("price") * detail.get("quantity") for detail in details])
        
        buy_voucher = BuyVoucher.objects.create(
            number=number,
            paid=paid,
            total=total,
            with_debt=with_debt,
            supplier=supplier
        )
        buy_voucher.create_details(details)
        
        return buy_voucher
    
    class Meta:
        model = BuyVoucher
        fields = ["number", "total", "paid", "rest", "with_debt", "supplier", "details"]
        read_only_fields = ["id", "total", "created_at", "updated_at"]