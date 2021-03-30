from django import dispatch
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Requisition
from library.models import Book,Item
from users.models import User,Profile
from django.core.mail import send_mail

def create_email(BookName,date):    
    date=str(date)
    return "Acabou de requisitat o livro : "+BookName+"a data limite de entrega é "+date 


@receiver(post_save, sender=Requisition,dispatch_uid="my_unique_identifier")
def post_save_requisition(sender,instance ,**kwargs):

    if kwargs['created']==True:
        print("signal!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print("new")
        #update state of the book
        content=Item.objects.get(pk=instance.item.pk)
        contentObject=content.content_object
        print(contentObject)
        contentObject.state="U"
        contentObject.save()
        # Item.objects.filter(pk=instance.item.pk).content_object.update(state='U')
        #update active requisitions in user
        profile=Profile.objects.get(pk=instance.user.pk)
        active_requisitions=profile.active_requisitions
        Profile.objects.filter(pk=instance.user.pk).update(active_requisitions=active_requisitions+1)
        print(kwargs)

        #snd email

        send_mail("Nova Requisição",create_email(contentObject.title,instance.deadline),"tlourenco9l@gmail.com",[profile.user.email],fail_silently= False)
    else:
        #update active requisitions -1
        if instance.state=="D":
            user=User.objects.get(pk=instance.user.pk)
            profile=Profile.objects.get(pk=instance.user.pk)
            active_requisitions=profile.active_requisitions
            Profile.objects.filter(pk=instance.user.pk).update(active_requisitions=active_requisitions-1)    
            

            #update book state
            contentObject=instance.item.content_object

            contentObject.state="A"
            contentObject.save()

            if profile.state=="U":
                requisitions=Requisition.objects.filter(user=user)
                if not requisitions.filter(state="DY").exists():
                    profile.state="A"
                    profile.save(update_fields=["state"])
        elif instance.state=="DY":
            profile=Profile.objects.get(pk=instance.user.pk)

            if profile.state != 'U':
                profile.state="U"
                profile.save(update_fields=["state"])



            print("from signal")
            print("Atrasado")


        
        


    

