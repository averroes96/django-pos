from django.urls import path, include

from rest_framework.routers import DefaultRouter

from products.views import ArticleViewSet, ArticleFamilyViewSet, ArticleBrandViewSet, UnitViewSet



router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename="articles")
router.register(r'families', ArticleFamilyViewSet, basename="families")
router.register(r'brands', ArticleBrandViewSet, basename="brands")
router.register(r'units', UnitViewSet, basename="units")

urlpatterns = [
    path("", include(router.urls))
]