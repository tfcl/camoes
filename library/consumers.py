from channels.generic.websocket import WebsocketConsumer
import logging
from asgiref.sync import async_to_sync, sync_to_async
from channels.consumer import AsyncConsumer
import asyncio
import json
from .models import Notification
from channels.db import database_sync_to_async
import asyncio
from .notificationLoop import send_Notifications
logger = logging.getLogger('django')



class notificationConsumer(WebsocketConsumer):
    groups = ["broadcast"]
    
       
         
    def websocket_connect(self, event):
        print("connected", event)
        
        
        self.accept()
        #     print(notification.pk)
        # await self.scope["session"].save()
        async_to_sync(self.channel_layer.group_add)(
            "notification",
            self.channel_name
        )

        for notification in Notification.objects.filter(isRead=False):
            self.send(text_data=json.dumps({
            'message': notification.subject
        }))
        

        

        self.send(text_data=json.dumps({
            'message': "Hello from consumer"
        }))
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']

        # To reject the connection, call:
        
    def websocket_message(self,event):
        message = event['message']

        print("messageTest",event)

        self.send(text_data=json.dumps({
            'message': message
        }))

    def websocket_receive(self,event ):
        print("receive",event)

    def websocket_disconnect(self,event):
        self.channel_layer.group_discard(
            "notification",
            self.channel_name
        )


        print("disconnected",event)
        # Called when the socket