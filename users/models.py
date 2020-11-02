from django.db import models

from django.contrib.auth.models import User
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    number=models.IntegerField(unique=True)
    telephone=models.IntegerField()
    adress=models.CharField(max_length=100 )




