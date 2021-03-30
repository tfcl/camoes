from django.db import models

from django.contrib.auth.models import User



class Profile(models.Model):
    user=models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    name=models.CharField('Nome',max_length=100,default='')
    contact=models.IntegerField('Contacto')
    address=models.CharField('Morada',max_length=100 )
    state=models.CharField('Estado',max_length=10,default='A' )
    active_requisitions=models.IntegerField(default=0,max_length=3)



