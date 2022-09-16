import decimal

from rest_framework.serializers import ModelSerializer

from products.models import Article, ArticleBrand, ArticleFamily, Unit


class ArticleFamilySerializer(ModelSerializer):
    
    class Meta:
        model = ArticleFamily
        fields = "__all__"


class ArticleBrandSerializer(ModelSerializer):
    
    class Meta:
        model = ArticleBrand
        fields = "__all__"


class UnitSerializer(ModelSerializer):

    class Meta:
        model = Unit
        fields = "__all__"


class ArticleSerializer(ModelSerializer):
    
    def create(self, validated_data):
        
        if validated_data.get("margin") != margin:
            buy_price = validated_data.get("buy_price")
            sell_price = validated_data.get("sell_price")
            margin = decimal.Decimal(((sell_price - buy_price) / buy_price) * 100)
        
        return Article.objects.create(margin=margin, **validated_data)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]