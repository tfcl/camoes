from django.core.mail import send_mail






def send_mail_to( message, receivers):
    send_mail("Atraso",message,"tlourenco9l@gmail.com",[receivers],fail_silently= False)