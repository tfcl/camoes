from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from library.models import Book
from django.contrib.auth.models import User
import channels.layers
from asgiref.sync import async_to_sync
import json



class Requisition(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    #end_date=models.DateTimeField(default=datetime.now()+timedelta(days=15))
    end_date=models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=20,default="Not Delivered")

    description = models.CharField(max_length=20)
    

class Notification(models.Model):
    subject=models.CharField(max_length=100)
    creationDate=models.DateTimeField(default=timezone.now)
    isRead=models.BooleanField(default=False)
    requisition=models.ForeignKey(Requisition, on_delete=models.CASCADE)
    print(requisition)
    #requisitionInstance=Requisition.objects.get(id=requisition)
    message=models.CharField(max_length=100)
    #message=models.CharField(max_length=100,default="O Livro"+requisitionInstance.book.title+"requisitado por"+requisitionInstance.user.username+"está atrasado")
    def save(self, *args, **kwargs):
        self.message="O Livro "+self.requisition.book.title+" requisitado por "+self.requisition.user.username+" está atrasado"
        
        super(Notification, self).save(*args, **kwargs)
        print(self.message)
def save_post(sender, instance ,**kwargs):
    
    # instance.isRead=True
    # message="O Livro"+instance.requisition.book.title+"requisitado por"+instance.requisition.user.username+"está atrasado"
    # print(message)
    # instance.message=message
    # instance.save(update_fields=['message'])


    channel_layer = channels.layers.get_channel_layer()
    subjectJs=instance.subject
    messageJs=instance.message
    requisitionJs=instance.requisition.pk
    message={"requisition":instance.requisition.book.title}
    message1={"notification":[instance.subject, instance.message,  instance.pk, instance.requisition.pk]}
    #print(message)
    # await channel_layer.send( {
    # "type": "message",
    # "text": "Hello there!"
    # })
    async_to_sync(channel_layer.group_send)(
    'notification',
    {'type': 'websocket_message','message':json.dumps({'message':messageJs, 'subject':subjectJs,'requisition':requisitionJs}) 
    })
    #
    # async_to_sync(channel_layer.send)("channel_name",{'type': 'library.websocket_message', 'message':'hello from signals1111111',})

post_save.connect(save_post, sender=Notification)