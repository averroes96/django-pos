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
    
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]