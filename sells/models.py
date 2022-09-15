from django.db import models

from base.models import Partner, Voucher, BaseModel

from products.models import Article

# Create your models here.


class Client(Partner):
    pass


class SellVoucher(Voucher):
    client = models.ForeignKey(to=Client, on_delete=models.DO_NOTHING)


class SellVoucherDetail(BaseModel):
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    article = models.ForeignKey(to=Article, on_delete=models.DO_NOTHING)
    voucher = models.ForeignKey(to=SellVoucher, related_name="details", on_delete=models.CASCADE)