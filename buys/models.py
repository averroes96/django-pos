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
                price=detail.get("price")
            )
    
    def update_details(self, details):
        
        detail_ids = []
        
        for detail in details:
            print(detail)
            if detail.get("id"):
                detail_ids.append(detail.get("id"))
                
                detail_object = self.details.get(id=detail.get("id"))
                detail_object.quantity = detail.get("quantity")
                detail_object.price = detail.get("price")
                detail_object.save()
            else:
                BuyVoucherDetail.objects.create(
                    voucher=self,
                    article=detail.get("article"),
                    quantity=detail.get("quantity"),
                    price=detail.get("price")
                )
        
        # delete removed details
        self.details.exclude(id__in=detail_ids).delete()


class BuyVoucherDetail(BaseModel):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_quantity = self.quantity
        self.current_price = self.price
    
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    article = models.ForeignKey(to=Article, on_delete=models.DO_NOTHING)
    voucher = models.ForeignKey(to=BuyVoucher, related_name="details", on_delete=models.CASCADE)