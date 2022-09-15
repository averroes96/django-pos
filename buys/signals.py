from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from buys.models import Supplier, BuyVoucher, BuyVoucherDetail


@receiver(pre_save, sender=Supplier)
def pre_supplier_save(sender, instance: Supplier, *args, **kwargs):
    
    if instance._state.adding and instance.balance: 
        instance.balance_initial = instance.balance


@receiver(post_save, sender=BuyVoucherDetail)
def post_buy_voucher_detail_save(sender, instance: BuyVoucherDetail, created, *args, **kwargs):
    
    article = instance.article
    
    if created:
        article.buy_price = instance.price
        article.quantity += instance.quantity
        article.save()


@receiver(pre_save, sender=BuyVoucher)
def pre_buy_voucher_save(sender, instance: BuyVoucher, *args, **kwargs):
    
    if instance._state.adding:
        instance.rest = instance.calculate_rest()
    


@receiver(post_save, sender=BuyVoucher)
def post_buy_voucher_save(sender, instance: BuyVoucher, created, *args, **kwargs):
    
    supplier = instance.supplier
    
    if created:
        supplier.balance += instance.total
        supplier.save()