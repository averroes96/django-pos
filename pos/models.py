from django.db import models

from base.models import Voucher, BaseModel

from sells.models import Client

from products.models import Article

# Create your models here.

class SaleVoucher(Voucher):
    
    client = models.ForeignKey(to=Client, on_delete=models.DO_NOTHING)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_rest = self.rest
    
    def create_details(self, details):
        """
        It creates a SaleVoucherDetail object for each detail in the details list
        
        :param details: This is a list of dictionaries. Each dictionary contains the following keys:
        """
        
        for detail in details:
            SaleVoucherDetail.objects.create(
                voucher=self,
                quantity=detail.get("quantity"),
                article=detail.get("article"),
                sell_price=detail.get("sell_price"),
                buy_price=detail.get("article").buy_price
            )
    
    def update_details(self, details):
        """
        > It updates the details of a sale voucher
        
        :param details: A list of dictionaries containing the details of the sale
        """
        
        detail_ids = []
        
        for detail in details:
            if detail.get("id"): # detail exists already
                detail_ids.append(detail.get("id"))
                
                detail_object = self.details.get(id=detail.get("id"))
                detail_object.quantity = detail.get("quantity")
                detail_object.sell_price = detail.get("sell_price")
                detail_object.save()
            else:
                SaleVoucherDetail.objects.create(
                    voucher=self,
                    article=detail.get("article"),
                    quantity=detail.get("quantity"),
                    sell_price=detail.get("sell_price"),
                    buy_price=detail.get("article").buy_price
                )
        
        # delete removed details
        self.details.exclude(id__in=detail_ids).delete()


class SaleVoucherDetail(BaseModel):
    
    quantity = models.PositiveIntegerField()
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    
    article = models.ForeignKey(to=Article, on_delete=models.DO_NOTHING)
    voucher = models.ForeignKey(to=SaleVoucher, related_name="details", on_delete=models.CASCADE)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_quantity = self.quantity