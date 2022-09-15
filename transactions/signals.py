from django.db.models.signals import post_save
from django.dispatch import receiver

from transactions.models import ClientTransaction, SupplierTransaction


@receiver(post_save, sender=ClientTransaction)
def post_client_transaction_save(sender, instance: ClientTransaction, created, *args, **kwargs):
    
    client = instance.client
    
    if created:
        client.balance += instance.value
        client.save()
    elif instance.current_value != instance.value:
        client.balance -= instance.current_value
        client.balance += instance.value
        client.save()


@receiver(post_save, sender=SupplierTransaction)
def post_supplier_transaction_save(sender, instance: SupplierTransaction, created, *args, **kwargs):
    
    supplier = instance.supplier
    
    if created:
        supplier.balance -= instance.value
        supplier.save()

    if instance.current_value != instance.value:
        supplier.balance += instance.current_value
        supplier.balance -= instance.value
        supplier.save()