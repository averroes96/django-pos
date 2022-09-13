from django.db import models

from base.models import BaseModel

# Create your models here.

class ProductFamily(BaseModel):
    name = models.CharField(max_length=128)


class Unit(BaseModel):
    name = models.CharField(max_length=64)


class Product(BaseModel):
    reference = models.CharField(max_length=128)
    name = models.CharField(max_length=256, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    quantity_minimum = models.PositiveIntegerField(default=0)
    stock_negative = models.BooleanField(default=False)
    margin = models.PositiveIntegerField(default=0)
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    
    family = models.ForeignKey(to=ProductFamily, null=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(to=Unit, null=True, on_delete=models.SET_NULL)