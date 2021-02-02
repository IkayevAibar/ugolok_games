import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer
import requests
import os

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # with open("data.json") as jsonfile:
        #     jsondata = json.load(jsonfile)
        # res = json.dumps(jsondata)
        # message.reply_channel.send({ "text": res, })
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        dic={
            'admin: start':0,
            'admin: stop':-1,
            'admin: pause':1,
        }
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': dic.get(message,"Error")
        }))

# # from channels import Group
# # from channels.sessions import channel_session
# from .models import Room

# @channel_session
# def ws_connect(message):
#     prefix, label = message['path'].strip('/').split('/')
#     room = Room.objects.get(label=label)
#     Group('chat-' + label).add(message.reply_channel)
#     message.channel_session['room'] = room.label

# @channel_session
# def ws_receive(message):
#     label = message.channel_session['room']
#     room = Room.objects.get(label=label)
#     data = json.loads(message['text'])
#     m = room.messages.create(handle=data['handle'], message=data['message'])
#     Group('chat-'+label).send({'text': json.dumps(m.as_dict())})

# @channel_session
# def ws_disconnect(message):
#     label = message.channel_session['room']
#     Group('chat-'+label).discard(message.reply_channel)