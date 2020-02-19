from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Messages,Chat
from django.contrib.auth import get_user_model
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        if self.scope['user'].is_staff:
            User = get_user_model()
            room_name = User.objects.get(username=self.room_name)
            room = Chat.objects.get(room_name=room_name)
        else:
            room = Chat.objects.get(room_name=self.scope['user'])
        Messages.objects.get_or_create(room=room,author=self.scope['user'], content=message)




    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Messages,Chat
from django.contrib.auth import get_user_model
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        if self.scope['user'].is_staff:
            User = get_user_model()
            room_name = User.objects.get(username=self.room_name)
            room = Chat.objects.get(room_name=room_name)
        else:
            room = Chat.objects.get(room_name=self.scope['user'])
        Messages.objects.get_or_create(room=room,author=self.scope['user'], content=message)




    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

