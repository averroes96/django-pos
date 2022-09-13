from django.db import models

from base.models import Partner, Voucher

# Create your models here.


class Client(Partner):
    pass


class SellVoucher(Voucher):
    client = models.ForeignKey(to=Client, null=True, on_delete=models.SET_NULL)