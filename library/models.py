from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
import channels.layers
from asgiref.sync import async_to_sync
logger = logging.getLogger('django')
import json

class Publisher(models.Model):
    name=models.CharField(max_length=100)
    adress=models.CharField(max_length=100)


class Author(models.Model):
    name=models.CharField(max_length=100)
    deathYear=models.IntegerField()
    birthYear=models.IntegerField()

class Book(models.Model):
    title=models.CharField(max_length=100)
    stock=models.CharField(max_length=100)
    year=models.IntegerField()
    classification=models.CharField(max_length=100)
    isbn=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    publisher=models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors=models.ManyToManyField(Author)
    



class Requisition(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    #end_date=models.DateTimeField(default=datetime.now()+timedelta(days=15))
    end_date=models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=20,default="Not Delivered")

    description = models.CharField(max_length=20)
    
    # def get_absolute_url(self):
    #     return reverse('requisition-detail', kwargs={'pk': self.pk})
    #deliver_dead=
    #deliver_date=
    #penalization

    


class Notification(models.Model):
    subject=models.CharField(max_length=100)
    message=models.CharField(max_length=100)
    creationDate=models.DateTimeField(default=timezone.now)
    isRead=models.BooleanField(default=False)
    requisition=models.ForeignKey(Requisition, on_delete=models.CASCADE)

def save_post(sender, instance ,**kwargs):
    
    # instance.isRead=True
    # instance.save()
  
    channel_layer = channels.layers.get_channel_layer()
    message={"requisition":instance.requisition.book.title}
    message1={"notification":[instance.subject, instance.pk, instance.requisition.pk]}
    #print(message)
    # await channel_layer.send( {
    # "type": "message",
    # "text": "Hello there!"
    # })
    async_to_sync(channel_layer.group_send)(
    'notification',
    {'type': 'websocket_message', 'message':json.dumps({'requisition':message['requisition'], 'instance':message1['notification']}) 
    })
    #
    # async_to_sync(channel_layer.send)("channel_name",{'type': 'library.websocket_message', 'message':'hello from signals1111111',})

post_save.connect(save_post, sender=Notification)