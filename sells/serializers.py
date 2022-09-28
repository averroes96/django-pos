from rest_framework.serializers import (
    ModelSerializer, 
    CharField,
    ValidationError
)

from sells.models import Client, SellVoucher, SellVoucherDetail
from sells.constants import SELL_DEBT_PERMISSION_ERROR

from agents.models import Agent


class SellVoucherDetailSerializer(ModelSerializer):
    
    id = CharField()
    
    class Meta:
        model = SellVoucherDetail
        fields = ["id", "article", "quantity", "sell_price"]


class SellVoucherDetailCreateSerializer(ModelSerializer):
    
    class Meta:
        model = SellVoucherDetail
        fields = ["article", "quantity", "sell_price"]


class SellVoucherListSerializer(ModelSerializer):
    
    class Meta:
        model = SellVoucher
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class SellVoucherCreateSerializer(ModelSerializer):
    
    details = SellVoucherDetailCreateSerializer(many=True)
    
    def validate(self, attrs):
        details = attrs.get("details")
        paid = attrs.get("paid")
        
        attrs["total"] = sum([
            detail.get("sell_price") * detail.get("quantity") for detail in details
        ]) # calculating voucher total
        with_debt = attrs["total"] > paid
        
        if not with_debt: # if not with debt ignore permission check
            return super().validate(attrs)
        
        user = self.context["request"].user
        
        if user.has_perm(f"agents.{Agent.Permission.SELLS_DEBT_PERMISSION_CODENAME}"):
            return super().validate(attrs)
        
        raise ValidationError(detail={"detail": SELL_DEBT_PERMISSION_ERROR.get("detail")})
    
    def create(self, validated_data):
        
        details = validated_data.get("details")
        
        paid = validated_data.get("paid") 
        with_debt = validated_data.get("with_debt", False)
        client = validated_data.get("client")
        number = validated_data.get("number")
        total = validated_data.get("total") # i'm passing the total through `.validate`
        agent = Agent.objects.get(user=self.context.get("request").user)
        
        sell_voucher = SellVoucher.objects.create(
            number=number,
            paid=paid,
            total=total,
            with_debt=with_debt,
            client=client,
            agent=agent
        )
        sell_voucher.create_details(details)
        
        return sell_voucher
    
    class Meta:
        model = SellVoucher
        fields = ["number", "total", "paid", "rest", "with_debt", "client", "agent" ,"details"]
        read_only_fields = ["id", "total", "created_at", "rest", "updated_at", "agent"]


class SellVoucherRetrieveSerializer(ModelSerializer):
    
    details = SellVoucherDetailSerializer(many=True)
    
    def validate(self, attrs):
        details = attrs.get("details")
        paid = attrs.get("paid")
        
        attrs["total"] = sum([
            detail.get("sell_price") * detail.get("quantity") for detail in details
        ]) # calculating voucher total
        with_debt = attrs["total"] > paid
        
        if not with_debt: # if not with debt ignore permission check
            return super().validate(attrs)
        
        user = self.context["request"].user
        
        if user.has_perm(f"agents.{Agent.Permission.SELLS_DEBT_PERMISSION_CODENAME}"):
            return super().validate(attrs)
        
        raise ValidationError(detail={"detail": SELL_DEBT_PERMISSION_ERROR.get("detail")})
    
    def update(self, instance, validated_data):
        details = validated_data.pop("details")
        
        instance.total = validated_data.get("total") # i'm passing the total through `.validate`
        instance.agent = Agent.objects.get(user=self.context.get("request").user)
        
        super().update(instance, validated_data)
        
        instance.update_details(details)
        
        return instance


    class Meta:
        model = SellVoucher
        fields = ["id", "number", "total", "paid", "rest", "with_debt", "client", "agent", "details"]
        read_only_fields = ["id", "total", "client", "agent", "rest", "created_at", "updated_at"]


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