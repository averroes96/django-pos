from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint

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
    
    reference = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    quantity_minimum = models.IntegerField(default=0) # used to alert stock
    stock_negative = models.BooleanField(default=False)
    margin = models.DecimalField(default="0.00", max_digits=10, decimal_places=2)
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    
    family = models.ForeignKey(to=ArticleFamily, null=True, blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(to=ArticleBrand, null=True, blank=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(to=Unit, null=True, blank=True, on_delete=models.SET_NULL)
    
    def infer_margin(self):
        """
        > The function `infer_margin` takes the `buy_price` and `sell_price` attributes of the `Product`
        class and calculates the margin as a percentage
        """
        import decimal
        
        try:
            self.margin = decimal.Decimal(((self.sell_price - self.buy_price) / self.buy_price) * 100)
        except ZeroDivisionError:
            self.margin = 0
    
    def __str__(self) -> str:
        return f"{self.reference}"
    
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(quantity__gte=0) & Q(stock_negative=False) & Q(quantity_minimum__gte=0), 
                name="check_stock"
            )
        ]