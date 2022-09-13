from django.db import models

from base.models import Partner, Voucher

# Create your models here.

class Supplier(Partner):
    pass

class BuyVoucher(Voucher):
    supplier = models.ForeignKey(to=Supplier, null=True, on_delete=models.SET_NULL)