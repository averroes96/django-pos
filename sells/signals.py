from django.db.models.signals import pre_save
from django.dispatch import receiver

from sells.models import Client



@receiver(pre_save, sender=Client)
def pre_client_save(sender, instance: Client, *args, **kwargs):
    
    if instance._state.adding and instance.balance: 
        instance.balance_initial = instance.balance