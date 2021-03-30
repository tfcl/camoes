import logging
from celery.schedules import crontab
from celery.task import periodic_task
from celery import Celery
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from camoes.myScripts import send_mail
from requisition.models import Requisition, Notification
from django.core.mail import send_mail
from datetime import timedelta  

logging.debug("Abriue")

app = Celery('tasks', broker='amqp://guest@localhost//')

def create_email(BookNumber):
    
    
    return "Por favor entregue o livro"+BookNumber+"no Centro de Camões"

@shared_task 
def check_requisitions():

    print("hello from worker")
    requisitions=Requisition.objects.filter(state='OG')
    date2 = datetime.now().date()+ timedelta(days=20) 
    #date2 = datetime.now().date()
    for requisition in requisitions:
        date1 = requisition.deadline.date()
        if date2 >= date1:
            

            requisition1=Requisition.objects.get(pk=requisition.pk)
            # requisition1=Requisition.objects.get(pk=requisition.pk)
            
            
            requisition1.state="DY"
            requisition1.save(update_fields=["state"]) 

            # print(requisition1.state)
            send_mail("Atraso",create_email(requisition.item.content_object.title),"tlourenco9l@gmail.com",[requisition.user.email],fail_silently= False)
            print(date2)
            
            
            newNotification= Notification(subject="atraso", message="O livro encontra-se atrasado", requisition=requisition)
            
            newNotification.save()
            

        
    #