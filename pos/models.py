from django.db import models

from base.models import Voucher

from sells.models import Client

# Create your models here.

class SaleVoucher(Voucher):
    client = models.ForeignKey(to=Client, null=True, on_delete=models.SET_NULL)