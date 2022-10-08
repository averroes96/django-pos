from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from sells.models import Client, SellVoucher, SellVoucherDetail



@receiver(pre_save, sender=Client)
def pre_client_save(sender, instance: Client, *args, **kwargs):
    
    if instance._state.adding and instance.balance: 
        instance.balance_initial = instance.balance


@receiver(post_save, sender=SellVoucherDetail)
def post_sell_voucher_detail_save(sender, instance: SellVoucherDetail, created, *args, **kwargs):
    
    article = instance.article
    
    if created:
        article.sell_price = instance.sell_price
        article.quantity -= instance.quantity
        article.save()
    elif (instance.current_quantity != instance.quantity):
        article.sell_price = instance.sell_price
        article.quantity += instance.current_quantity
        article.quantity -= instance.quantity
        article.save()


@receiver(pre_delete, sender=SellVoucherDetail)
def pre_sell_voucher_detail_delete(sender, instance: SellVoucherDetail, *args, **kwargs):
    instance.article.quantity += instance.quantity
    instance.article.save()


@receiver(pre_save, sender=SellVoucher)
def pre_sell_voucher_save(sender, instance: SellVoucher, *args, **kwargs):
    instance.rest = instance.calculate_rest()
    instance.with_debt = instance.paid < instance.total


@receiver(post_save, sender=SellVoucher)
def post_sell_voucher_save(sender, instance: SellVoucher, created, *args, **kwargs):
    
    client = instance.client
    
    if created:
        client.balance += instance.rest
        client.save()
    elif instance.current_rest != instance.rest:
        client.balance -= instance.current_rest
        client.balance += instance.rest
        client.save()