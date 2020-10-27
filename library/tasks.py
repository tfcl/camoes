import logging
from celery.schedules import crontab
from celery.task import periodic_task
from celery import Celery
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from camoes.myScripts import send_mail
from .models import Requisition, Notification
from django.core.mail import send_mail


logging.debug("Abriue")

app = Celery('tasks', broker='amqp://guest@localhost//')

def create_email(BookNumber):
    
    
    return "Por favor entregue o livro"+BookNumber+"no Centro de Camões"

@shared_task 
def check_requisitions():
    requisitions=Requisition.objects.filter(state='Not Delivered')
    
    date2 = datetime.now().date()
    for requisition in requisitions:
        date1 = requisition.end_date.date()
        if date2 >= date1:
            
            Requisition.objects.filter(pk=requisition.pk).update(state="Delayed")
            
            send_mail("Atraso",create_email(requisition.book.title),"tlourenco9l@gmail.com",[requisition.user.email],fail_silently= False)
            print(date2)
            
            print(requisition.end_date)
            
            newNotification= Notification(subject="atraso", message="O livro encontra-se atrasado", requisition=requisition)
            
            newNotification.save()
            

        
    #