from rest_framework.serializers import (
    ModelSerializer, 
    CharField, 
    CurrentUserDefault, 
    PrimaryKeyRelatedField,
    ValidationError
)

from buys.models import Supplier, BuyVoucher, BuyVoucherDetail
from buys.constants import BUY_DEBT_PERMISSION_ERROR

from agents.models import Agent



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


class BuyVoucherDetailSerializer(ModelSerializer):
    
    id = CharField()
    
    class Meta:
        model = BuyVoucherDetail
        fields = ["id", "article", "quantity", "buy_price", "sell_price"]

class BuyVoucherDetailCreateSerializer(ModelSerializer):
    
    class Meta:
        model = BuyVoucherDetail
        fields = ["article", "quantity", "buy_price", "sell_price"]


class BuyVoucherListSerializer(ModelSerializer):
    
    class Meta:
        model = BuyVoucher
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class BuyVoucherCreateSerializer(ModelSerializer):
    
    details = BuyVoucherDetailCreateSerializer(many=True)
    
    def validate(self, attrs):
        details = attrs.get("details")
        paid = attrs.get("paid")
        
        attrs["total"] = sum([
            detail.get("buy_price") * detail.get("quantity") for detail in details
        ]) # calculating voucher total
        with_debt = attrs["total"] > paid
        
        if not with_debt: # if not with debt ignore permission check
            return super().validate(attrs)
        
        user = self.context["request"].user
        
        if user.has_perm(f"agents.{Agent.Permission.BUYS_DEBT_PERMISSION_CODENAME}"):
            return super().validate(attrs)
        
        raise ValidationError(detail={"detail": BUY_DEBT_PERMISSION_ERROR.get("detail")})
    
    def create(self, validated_data):
        
        details = validated_data.get("details")
        
        paid = validated_data.get("paid")
        with_debt = validated_data.get("with_debt", False)
        supplier = validated_data.get("supplier")
        number = validated_data.get("number")
        
        agent = Agent.objects.get(user=self.context.get("request").user)
        total = validated_data.get("total") # i'm passing the total through `.validate`
        
        buy_voucher = BuyVoucher.objects.create(
            number=number,
            paid=paid,
            total=total,
            with_debt=with_debt,
            supplier=supplier,
            agent=agent
        )
        buy_voucher.create_details(details)
        
        return buy_voucher
    
    class Meta:
        model = BuyVoucher
        fields = ["number", "total", "paid", "rest", "with_debt", "supplier", "agent" ,"details"]
        read_only_fields = ["id", "total", "created_at", "rest", "updated_at", "agent"]


class BuyVoucherRetrieveSerializer(ModelSerializer):
    
    details = BuyVoucherDetailSerializer(many=True)
    agent = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    
    def validate(self, attrs):
        details = attrs.get("details")
        paid = attrs.get("paid")
        
        attrs["total"] = sum([
            detail.get("buy_price") * detail.get("quantity") for detail in details
        ]) # calculating voucher total
        with_debt = attrs["total"] > paid
        
        if not with_debt: # if not with debt ignore permission check
            return super().validate(attrs)
        
        user = self.context["request"].user
        
        if user.has_perm(f"agents.{Agent.Permission.BUYS_DEBT_PERMISSION_CODENAME}"):
            return super().validate(attrs)
        
        raise ValidationError(detail={"detail": BUY_DEBT_PERMISSION_ERROR.get("detail")})
    
    def update(self, instance, validated_data):
        details = validated_data.pop("details")
        instance.agent = Agent.objects.get(user=self.context.get("request").user)
        instance.total = validated_data.get("total") # i'm passing the total through `.validate`
        
        super().update(instance, validated_data)
        
        instance.update_details(details)
        
        return instance
    
    class Meta:
        model = BuyVoucher
        fields = ["id", "number", "total", "paid", "rest", "with_debt", "supplier", "agent", "details"]
        read_only_fields = ["id", "total", "supplier", "agent", "rest", "created_at", "updated_at"]