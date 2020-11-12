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
    @classmethod
    def create(cls, name):
        publisher = cls(name=name)
        # do something with the book
        return publisher
class Author(models.Model):
  
    name=models.CharField(max_length=100)
    deathYear=models.IntegerField(blank=True, null=True)
    birthYear=models.IntegerField(blank=True, null=True)

class Book(models.Model):
    title=models.CharField(max_length=100)
    stock=models.CharField(max_length=100)
    year=models.IntegerField()
    classification=models.CharField(max_length=100)
    isbn=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    publisher=models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors=models.ManyToManyField(Author)
    



    

