from rest_framework.serializers import ModelSerializer

from products.models import Product, ProductFamily, Unit


class ProductFamilySerializer(ModelSerializer):
    
    class Meta:
        model = ProductFamily
        fields = "__all__"


class UnitSerializer(ModelSerializer):

    class Meta:
        model = Unit
        fields = "__all__"


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"