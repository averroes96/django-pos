from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from pos.models import SaleVoucher, SaleVoucherDetail

@receiver(post_save, sender=SaleVoucherDetail)
def post_sale_voucher_detail_save(sender, instance: SaleVoucherDetail, created, *args, **kwargs):
    
    article = instance.article
    
    if created:
        article.quantity -= instance.quantity
        article.save()
    elif (instance.current_quantity != instance.quantity):
        article.quantity += instance.current_quantity
        article.quantity -= instance.quantity
        article.save()


@receiver(pre_save, sender=SaleVoucher)
def pre_sale_voucher_save(sender, instance: SaleVoucher, *args, **kwargs):
    instance.rest = instance.calculate_rest()
    instance.with_debt = instance.paid < instance.total


@receiver(post_save, sender=SaleVoucher)
def post_sale_voucher_save(sender, instance: SaleVoucher, created, *args, **kwargs):
    
    client = instance.client
    
    if created:
        client.balance += instance.rest
        client.save()
    elif instance.current_rest != instance.rest:
        client.balance -= instance.current_rest
        client.balance += instance.rest
        client.save()