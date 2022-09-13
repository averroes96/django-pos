from django.db.models.signals import pre_save
from django.dispatch import receiver

from buys.models import Supplier


@receiver(pre_save, sender=Supplier)
def pre_supplier_save(sender, instance: Supplier, *args, **kwargs):
    
    if instance._state.adding and instance.balance_initial: 
        instance.balance = instance.balance_initial