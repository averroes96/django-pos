from django.contrib import admin

from products.models import ArticleBrand, Article, ArticleFamily, Unit

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    list_display = ["__str__", "buy_price", "sell_price", "quantity", "family", "brand", "unit"]
    search_fields = ["__str__", "name"]
    list_filter = ["family", "brand", "unit"]
    list_per_page = 16

@admin.register(ArticleFamily)
class ArticleFamilyAdmin(admin.ModelAdmin):
    
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 16


@admin.register(ArticleBrand)
class ArticleBrandAdmin(admin.ModelAdmin):
    
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 16


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 16