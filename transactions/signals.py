from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.transaction import atomic

from transactions.models import ClientTransaction, SupplierTransaction


@receiver(post_save, sender=ClientTransaction)
@atomic
def post_client_transaction_save(sender, instance: ClientTransaction, created, *args, **kwargs):
    
    client = instance.client
    
    if created:
        client.balance -= instance.value
        client.save()
    elif instance.current_value != instance.value:
        client.balance += instance.current_value
        client.balance -= instance.value
        client.save()


@receiver(pre_delete, sender=ClientTransaction)
@atomic
def pre_client_transaction_delete(sender, instance: ClientTransaction, *args, **kwargs):
    
    client = instance.client
    
    client.balance += instance.value
    client.save()

@receiver(post_save, sender=SupplierTransaction)
@atomic
def post_supplier_transaction_save(sender, instance: SupplierTransaction, created, *args, **kwargs):
    
    supplier = instance.supplier
    
    if created:
        supplier.balance -= instance.value
        supplier.save()

    if instance.current_value != instance.value:
        supplier.balance += instance.current_value
        supplier.balance -= instance.value
        supplier.save()


@receiver(pre_delete, sender=SupplierTransaction)
@atomic
def pre_supplier_transaction_delete(sender, instance: SupplierTransaction, *args, **kwargs):
    
    supplier = instance.client
    
    supplier.balance += instance.value
    supplier.save()