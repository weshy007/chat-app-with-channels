import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template

from .models import Room, Message


class TalkConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None
        self.group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'chat_{self.room}'
        self.room = Room.objects.get(id=self.room_name)
        self.user = self.scope['user']

        # Accepting Connection
        self.accept()

        # Joinging a group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        # User joined notification
        html = get_template('join.hmtl').render(context={'user': self.user})
        self.send(text_data=html)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        html = get_template('leave.hmtl').render(context={'user': self.user})
        self.send(
            text_data=html
        )
        self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        room = Room.objects.get(id=self.room_name)
        Message.objects.create(user=self.user, room=room, content=text_data_json['message'])

        html = get_template('chats.html').render(context={'messages': room.message_set.all()})
        self.send(text_data=html)
        