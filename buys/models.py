from django.db import models

from base.models import Partner, Voucher, BaseModel

from products.models import Article

# Create your models here.

class Supplier(Partner):
    pass

class BuyVoucher(Voucher):
    supplier = models.ForeignKey(to=Supplier, on_delete=models.DO_NOTHING)
    
    def create_details(self, details):
        """
        It creates a list of BuyVoucherDetail objects from a list of dictionaries
        
        :param details: list of dictionaries
        """
        details_list = []
        
        for detail in details:
            details_list.append(
                BuyVoucherDetail.objects.create(
                    voucher=self,
                    quantity=detail.get("quantity"),
                    article=detail.get("article"),
                    price=detail.get("price")
                )
            )


class BuyVoucherDetail(BaseModel):
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    article = models.ForeignKey(to=Article, on_delete=models.DO_NOTHING)
    voucher = models.ForeignKey(to=BuyVoucher, related_name="details", on_delete=models.CASCADE)