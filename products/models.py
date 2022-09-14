from django.db import models

from base.models import BaseModel

# Create your models here.


class ArticleFamily(BaseModel):
    name = models.CharField(max_length=128)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Article families"


class ArticleBrand(BaseModel):
    name = models.CharField(max_length=128)
    
    def __str__(self) -> str:
        return self.name


class Unit(BaseModel):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class Article(BaseModel):
    reference = models.CharField(max_length=128)
    name = models.CharField(max_length=256, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    quantity_minimum = models.PositiveIntegerField(default=0)
    stock_negative = models.BooleanField(default=False)
    margin = models.PositiveIntegerField(default=0)
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    
    family = models.ForeignKey(to=ArticleFamily, null=True, blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(to=ArticleBrand, null=True, blank=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(to=Unit, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self) -> str:
        return f"{self.reference}" 