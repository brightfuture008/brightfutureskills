import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        
        if not self.user.is_authenticated:
            await self.close()
            return

        # Sort IDs to create a consistent room name for the pair
        users = sorted([int(self.user.id), int(self.other_user_id)])
        self.room_group_name = f'chat_{users[0]}_{users[1]}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"WebSocket connected: {self.room_group_name}")
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        # Handle typing events
        if 'typing' in text_data_json:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'sender_id': self.user.id,
                    'typing': text_data_json['typing']
                }
            )
            return

        message = text_data_json.get('message', '')
        if not message:
            return
        
        # Save message to database
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'sender_username': self.user.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender_id': event['sender_id'],
            'typing': event['typing']
        }))

    @database_sync_to_async
    def save_message(self, message):
        other_user = User.objects.get(id=self.other_user_id)
        ChatMessage.objects.create(
            sender=self.user,
            receiver=other_user,
            message=message
        )