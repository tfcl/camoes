import channels.layers
from asgiref.sync import async_to_sync
from .models import Notification
import json

def send_Notifications():
    notifications=Notification.objects.filter(isRead=False)
    print(notifications)
    
    for notification in notifications:
        
        async_to_sync(channel_layer.group_send)(
            'notification',
            {'type': 'websocket_message', 'message':'hello from loop'
        })