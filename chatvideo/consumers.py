import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoChatConsumer(AsyncWebsocketConsumer):
    rooms = {}  # stocke la liste des sockets par room

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"videochat_{self.room_name}"

        # Ajouter au groupe
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Déterminer le rôle
        if self.room_group_name not in VideoChatConsumer.rooms:
            VideoChatConsumer.rooms[self.room_group_name] = []

        VideoChatConsumer.rooms[self.room_group_name].append(self.channel_name)

        # Premier connecté = offerer
        is_initiator = len(VideoChatConsumer.rooms[self.room_group_name]) == 1

        await self.send(text_data=json.dumps({
            "type": "init_role",
            "isOfferer": is_initiator
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if self.room_group_name in VideoChatConsumer.rooms:
            if self.channel_name in VideoChatConsumer.rooms[self.room_group_name]:
                VideoChatConsumer.rooms[self.room_group_name].remove(self.channel_name)

            # Nettoyage si vide
            if not VideoChatConsumer.rooms[self.room_group_name]:
                del VideoChatConsumer.rooms[self.room_group_name]

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'video_chat_message',
                'message': text_data,
                'sender': self.channel_name
            }
        )

    async def video_chat_message(self, event):
        # Ne pas renvoyer à soi-même
        if event['sender'] != self.channel_name:
            await self.send(text_data=event['message'])
