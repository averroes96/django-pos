from django.db import models

from base.models import Partner, Voucher, BaseModel

from products.models import Article

# Create your models here.


class Client(Partner):
    pass


class SellVoucher(Voucher):
    
    client = models.ForeignKey(to=Client, on_delete=models.DO_NOTHING)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_rest = self.rest
    
    def create_details(self, details):
        """
        It creates a list of BuyVoucherDetail objects from a list of dictionaries
        
        :param details: list of dictionaries
        """
        
        for detail in details:
            SellVoucherDetail.objects.create(
                voucher=self,
                quantity=detail.get("quantity"),
                article=detail.get("article"),
                sell_price=detail.get("sell_price"),
                buy_price=detail.get("article").buy_price
            )
    
    def update_details(self, details):
        
        detail_ids = []
        
        for detail in details:
            if detail.get("id"):
                detail_ids.append(detail.get("id"))
                
                detail_object = self.details.get(id=detail.get("id"))
                detail_object.quantity = detail.get("quantity")
                detail_object.sell_price = detail.get("sell_price")
                detail_object.save()
            else:
                SellVoucherDetail.objects.create(
                    voucher=self,
                    article=detail.get("article"),
                    quantity=detail.get("quantity"),
                    sell_price=detail.get("sell_price"),
                    buy_price=detail.get("article").buy_price
                )
        
        # delete removed details
        self.details.exclude(id__in=detail_ids).delete()
    
    class Meta:
        get_latest_by = ['created_at']
        ordering = ['-created_at']

class SellVoucherDetail(BaseModel):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_quantity = self.quantity
        self.current_sell_price = self.sell_price
    
    quantity = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    buy_price = models.PositiveIntegerField()
    
    article = models.ForeignKey(to=Article, on_delete=models.DO_NOTHING)
    voucher = models.ForeignKey(to=SellVoucher, related_name="details", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.voucher} ({self.article})"