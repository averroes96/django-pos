from django.db.models.signals import post_save
from django.dispatch import receiver

from transactions.models import ClientTransaction, SupplierTransaction


@receiver(post_save, sender=ClientTransaction)
def post_client_transaction_save(sender, instance: ClientTransaction, *args, **kwargs):
    
    if instance._state.adding:
        client = instance.client
        client.balance += instance.value
        client.save()


@receiver(post_save, sender=SupplierTransaction)
def post_supplier_transaction_save(sender, instance: SupplierTransaction, *args, **kwargs):
    
    if instance._state.adding:
        supplier = instance.supplier
        supplier.balance -= instance.value
        supplier.save()