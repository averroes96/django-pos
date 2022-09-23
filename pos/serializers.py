from rest_framework.serializers import (
    ModelSerializer, 
    CharField, 
    PrimaryKeyRelatedField, 
    CurrentUserDefault,
)
from rest_framework.serializers import ValidationError

from django.db.transaction import atomic

from pos.models import SaleVoucher, SaleVoucherDetail
from pos.constants import DETAIL_CANNOT_BE_EMPTY

from agents.models import Agent



class SaleVoucherDetailSerializer(ModelSerializer):
    
    id = CharField()
    
    class Meta:
        model = SaleVoucherDetail
        fields = ["id", "article", "quantity", "sell_price", "buy_price"]


class SaleVoucherDetailCreateSerializer(ModelSerializer):
    
    class Meta:
        model = SaleVoucherDetail
        fields = ["article", "quantity", "sell_price"]


class SaleVoucherListSerializer(ModelSerializer):
    
    class Meta:
        model = SaleVoucher
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class SaleVoucherCreateSerializer(ModelSerializer):
    
    details = SaleVoucherDetailCreateSerializer(required=True, many=True)
    agent = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault()) # useless
    
    def validate(self, attrs):
        details = attrs.get("details")
        
        if not details: raise ValidationError({"detail": DETAIL_CANNOT_BE_EMPTY})   
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        
        details = validated_data.get("details")
        
        paid = validated_data.get("paid")
        with_debt = validated_data.get("with_debt", False)
        client = validated_data.get("client")
        number = validated_data.get("number")
        
        agent = Agent.objects.get(user=self.context.get("request").user)
        total = sum([detail.get("sell_price") * detail.get("quantity") for detail in details])
        
        sale_voucher = SaleVoucher.objects.create(
            number=number,
            paid=paid,
            total=total,
            with_debt=with_debt,
            client=client,
            agent=agent
        )
        sale_voucher.create_details(details)
        
        return sale_voucher
    
    class Meta:
        model = SaleVoucher
        fields = ["number", "total", "paid", "rest", "with_debt", "client", "agent" ,"details"]
        read_only_fields = ["id", "total", "created_at", "rest", "updated_at", "agent"]


class SaleVoucherRetrieveSerializer(ModelSerializer):
    
    details = SaleVoucherDetailSerializer(many=True)
    agent = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault()) # useless
    
    def validate(self, attrs):
        details = attrs.get("details")
        
        if not details: raise ValidationError({"detail": DETAIL_CANNOT_BE_EMPTY})
        
        return super().validate(attrs)
    
    @atomic
    def update(self, instance, validated_data):
        
        details = validated_data.pop("details")
        instance.total = sum([detail.get("sell_price") * detail.get("quantity") for detail in details])
        instance.agent = Agent.objects.get(user=self.context.get("request").user)
        
        super().update(instance, validated_data)
        instance.update_details(details)
        
        return instance


    class Meta:
        model = SaleVoucher
        fields = ["id", "number", "total", "paid", "rest", "with_debt", "client", "agent", "details"]
        read_only_fields = ["id", "total", "client", "agent", "rest", "created_at", "updated_at"]