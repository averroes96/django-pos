from rest_framework.viewsets import ModelViewSet

from products.models import Article, ArticleFamily, ArticleBrand, Unit
from products.serializers import ArticleBrandSerializer, ArticleFamilySerializer, ArticleSerializer, UnitSerializer

from agents.permissions import IsAdminOrAgent

# Create your views here.


class ArticleFamilyViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ArticleFamilySerializer
    
    def get_queryset(self):
        return ArticleFamily.objects.all()


class ArticleBrandViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ArticleBrandSerializer
    
    def get_queryset(self):
        return ArticleBrand.objects.all()


class UnitViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = UnitSerializer
    
    def get_queryset(self):
        return Unit.objects.all() 


class ArticleViewSet(ModelViewSet):
    
    permission_classes = [IsAdminOrAgent]
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        return Article.objects.all() 