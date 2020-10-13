from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    #deliver_dead=
    #deliver_date=
    #penalization

    


