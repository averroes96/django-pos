from django.db import models

from base.models import Partner, Voucher, BaseModel

from products.models import Article

# Create your models here.

class Supplier(Partner):
    pass

class BuyVoucher(Voucher):
    
    supplier = models.ForeignKey(to=Supplier, on_delete=models.DO_NOTHING)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_rest = self.rest
    
    def __str__(self) -> str:
        return self.number
    
    def create_details(self, details):
        """
        It creates a list of BuyVoucherDetail objects from a list of dictionaries
        
        :param details: list of dictionaries
        """
        
        for detail in details:
            BuyVoucherDetail.objects.create(
                voucher=self,
                quantity=detail.get("quantity"),
                article=detail.get("article"),
                buy_price=detail.get("buy_price"),
                sell_price=detail.get("sell_price")
            )
    
    def update_details(self, details):
        """
        It updates the details of a buy voucher
        
        :param details: This is a list of dictionaries. Each dictionary represents a detail of the voucher
        """
        
        detail_ids = []
        
        for detail in details:
            if detail.get("id"):
                detail_ids.append(detail.get("id"))
                
                detail_object = self.details.get(id=detail.get("id"))
                detail_object.quantity = detail.get("quantity")
                detail_object.buy_price = detail.get("buy_price")
                detail_object.sell_price = detail.get("sell_price")
                detail_object.save()
            else:
                BuyVoucherDetail.objects.create(
                    voucher=self,
                    article=detail.get("article"),
                    quantity=detail.get("quantity"),
                    buy_price=detail.get("buy_price"),
                    sell_price=detail.get("sell_price")
                )
        
        # delete removed details
        self.details.exclude(id__in=detail_ids).delete()

    class Meta:
        get_latest_by = ['created_at']
        ordering = ['-created_at']

class BuyVoucherDetail(BaseModel):
    
    quantity = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    buy_price = models.PositiveIntegerField()
    
    article = models.ForeignKey(to=Article, on_delete=models.DO_NOTHING)
    voucher = models.ForeignKey(to=BuyVoucher, related_name="details", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.voucher} ({self.article})"