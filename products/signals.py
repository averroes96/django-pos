from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import Article


@receiver(pre_save, sender=Article)
def pre_article_save(sender, instance: Article, *args, **kwargs):
    instance.infer_margin()