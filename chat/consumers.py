import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timesince

from .models import ChatRoom, Message
from users.models import LitterUser


class ChatConsumer(WebsocketConsumer):
    def create_chat(self, msg, pk):
        room = ChatRoom.objects.get(uuid=self.room_group_name)
        sender = LitterUser.objects.get(id=pk)
        return Message.objects.create(chatroom=room,
                                      user=sender,
                                      text=msg)

    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['pk']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json['pk']
        message = text_data_json['message']

        message = self.create_chat(message, sender)
        msg = str(message.text)
        sender = str(message.user.username)
        sent = str(timesince.timesince(message.sent))
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg,
                'sender': sender,
                'sent': sent
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender'],
            'sent': event['sent']
        }))
# TODO make the connection not timeout as long as user is on the page
