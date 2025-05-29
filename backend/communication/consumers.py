import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Check if user is authenticated and part of the chat
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
            return
        
        is_participant = await self.is_user_in_chat(user.id, self.chat_id)
        if not is_participant:
            await self.close()
            return

        # Join chat group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        user = self.scope['user']
        if not message:
            return

        # Save message to DB
        msg = await self.create_message(user.id, self.chat_id, message)

        # Send message to group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': msg.text,
                'username': user.username,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'message_id': msg.id,
            }
        )

    # Receive message from group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))

    @database_sync_to_async
    def is_user_in_chat(self, user_id, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            return chat.participants.filter(id=user_id).exists()
        except Chat.DoesNotExist:
            return False

    @database_sync_to_async
    def create_message(self, user_id, chat_id, message_text):
        user = User.objects.get(id=user_id)
        chat = Chat.objects.get(id=chat_id)
        return Message.objects.create(chat=chat, sender=user, text=message_text)
