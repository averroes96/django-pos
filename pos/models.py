from django.db import models

from base.models import Voucher, BaseModel

from sells.models import Client

from products.models import Article

# Create your models here.

class SaleVoucher(Voucher):
    
    client = models.ForeignKey(to=Client, null=True, on_delete=models.SET_NULL)


class SaleVoucherDetail(BaseModel):
    quantity = models.PositiveIntegerField()
    
    article = models.ForeignKey(to=Article, on_delete=models.DO_NOTHING)
    voucher = models.ForeignKey(to=SaleVoucher, related_name="details", on_delete=models.CASCADE)