from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category

@receiver([post_save,post_delete],sender=Category)
def invalid_cach_categories(sender,instance ,*args,**kwargs):
    print('clear')
    cache.clear()