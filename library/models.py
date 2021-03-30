from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
import channels.layers
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


logger = logging.getLogger('django')
import json



class Publisher(models.Model):
    name=models.CharField(max_length=100)
    adress=models.CharField(max_length=100,blank=True, null=True)


    @classmethod
    def create(cls, name,adress):
        publisher = cls(name=name,adress=adress)
        # do something with the book
        return publisher



class Author(models.Model):
  
    name=models.CharField(max_length=100)
    deathYear=models.IntegerField(blank=True, null=True)
    birthYear=models.IntegerField(blank=True, null=True)


    def __str__(self):
        firstName=""
        lastName=""

        tempName=self.name.split(" ")
        print(tempName)
        lastName=tempName[-1]

        for i in range(0,len(tempName)-1):
           
              

             
            firstName+=tempName[i]+" "
        string=lastName+", "+firstName
        
        if self.birthYear:
            string=string+"("+str(self.birthYear)+"-"
            if self.deathYear:
                string+=str(self.deathYear)+")"
            else:
                string+=")"
        # print("from model!!!")
        # print(string)
        # print(firstName)
        return string

    @classmethod
    def create(cls, name,birthYear, deathYear):
        author = cls(name=name,birthYear=birthYear,deathYear=deathYear)
        
        # do something with the book
        return author

class Category(models.Model):
    name=models.CharField(max_length=100)
    parentPk=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    depth=models.IntegerField(default=0)
    udc=models.IntegerField()
    def __str__(self):
        return self.name








class Type(models.Model):
    control_letter=models.CharField(max_length=100)
    type=models.CharField(max_length=100)


class Item(models.Model):


    limit = Q(app_label = 'library', model = 'magazine') | Q(app_label = 'library', model = 'book')
    identifier=models.IntegerField(default=0)
    
    type=models.ForeignKey(Type,  on_delete=models.CASCADE)


    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    def __str__(self):
        
        string=str(self.identifier)+" "+self.type.control_letter
        return string




class Magazine(models.Model):
    title=models.CharField(max_length=100)
    edition_number=models.IntegerField(null=True)
    issn=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    state=models.CharField(max_length=100,default='A')

    Item = GenericRelation(Item)




class Book(models.Model):
    title=models.CharField(max_length=100)
    stock=models.CharField(max_length=100, default="")
    year=models.IntegerField(null=True)
    classification=models.CharField(max_length=100)
    isbn=models.CharField(max_length=100)
    state=models.CharField(max_length=100,default='A')
    publisher=models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors=models.ManyToManyField(Author)
    category=models.ForeignKey(Category,null=True, on_delete=models.CASCADE)
    Item = GenericRelation(Item)

    @classmethod
    def create(cls, title,publisher,category,year,isbn):
        book = cls(title=title,publisher=publisher,category=category,year=year,isbn=isbn )
        
        # do something with the book
        return book

