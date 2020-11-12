from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Requisition
from library.models import Book

@receiver(post_save, sender=Requisition)
def post_save_requisition(sender,instance ,**kwargs):


    print("signals_Requisition")
    print(instance)
    Book.objects.filter(pk=instance.book.pk).update(status='Unavailable')
    print(Book.objects.get(pk=instance.book.pk).status)


    

