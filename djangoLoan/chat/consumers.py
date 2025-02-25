import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import CustomUser
from .models import ChatMessage
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Rejoindre le groupe de chat
        await self.channel_layer.group_add(
            "chat_general",
            self.channel_name
        )
        await self.accept()
        
        # Si l'utilisateur est authentifié, envoyer un message de connexion
        if self.scope.get('user') and self.scope['user'].is_authenticated:
            user_email = self.scope['user'].email
            await self.channel_layer.group_send(
                "chat_general",
                {
                    'type': 'user_join',
                    'user': user_email
                }
            )
    
    async def disconnect(self, close_code):
        # Quitter le groupe de chat
        await self.channel_layer.group_discard(
            "chat_general",
            self.channel_name
        )
        
        # Si l'utilisateur est authentifié, envoyer un message de déconnexion
        if self.scope.get('user') and self.scope['user'].is_authenticated:
            user_email = self.scope['user'].email
            await self.channel_layer.group_send(
                "chat_general",
                {
                    'type': 'user_leave',
                    'user': user_email
                }
            )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        
        if message and self.scope.get('user') and self.scope['user'].is_authenticated:
            user = self.scope['user']
            
            # Enregistrer le message dans la base de données
            await self.save_message(user, message)
            
            # Envoyer le message au groupe
            await self.channel_layer.group_send(
                "chat_general",
                {
                    'type': 'chat_message',
                    'message': {
                        'content': message,
                        'user_email': user.email,
                        'timestamp': timezone.now().strftime('%d-%m-%Y %H:%M'),
                        'is_staff': user.is_staff
                    }
                }
            )
    
    async def chat_message(self, event):
        message = event['message']
        
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))
    
    async def user_join(self, event):
        # Envoyer l'information de connexion d'utilisateur
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'user': event['user']
        }))
    
    async def user_leave(self, event):
        # Envoyer l'information de déconnexion d'utilisateur
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'user': event['user']
        }))
    
    @database_sync_to_async
    def save_message(self, user, content):
        return ChatMessage.objects.create(
            user=user,
            content=content
        )
















# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from accounts.models import CustomUser
# from .models import ChatMessage

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = "chat_general"
        
#         # Vérifier si l'utilisateur est authentifié
#         if not self.scope.get('user') or not self.scope['user'].is_authenticated:
#             await self.close()
#             return
            
#         # Rejoindre le groupe de chat
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
        
#         await self.accept()
        
#         # Informer les autres utilisateurs qu'un nouvel utilisateur est connecté
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'user_join',
#                 'user': self.scope['user'].email,
#                 'is_staff': self.scope['user'].is_staff
#             }
#         )
    
#     async def disconnect(self, close_code):
#         # Quitter le groupe
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
        
#         # Informer les autres utilisateurs qu'un utilisateur s'est déconnecté
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'user_leave',
#                 'user': self.scope['user'].email if self.scope.get('user') else "Unknown"
#             }
#         )
    
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
        
#         # Stocker le message dans la base de données
#         await self.save_message(message)
        
#         # Envoyer le message au groupe
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': {
#                     'content': message,
#                     'user_email': self.scope['user'].email,
#                     'timestamp': await self.get_timestamp(),
#                     'is_staff': self.scope['user'].is_staff
#                 }
#             }
#         )
    
#     async def chat_message(self, event):
#         message = event['message']
        
#         # Envoyer le message au WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'message',
#             'message': message
#         }))
    
#     async def user_join(self, event):
#         # Informer le client qu'un utilisateur a rejoint
#         await self.send(text_data=json.dumps({
#             'type': 'user_join',
#             'user': event['user'],
#             'is_staff': event['is_staff']
#         }))
    
#     async def user_leave(self, event):
#         # Informer le client qu'un utilisateur est parti
#         await self.send(text_data=json.dumps({
#             'type': 'user_leave',
#             'user': event['user']
#         }))
    
#     @database_sync_to_async
#     def save_message(self, content):
#         user = self.scope['user']
#         ChatMessage.objects.create(user=user, content=content)
    
#     @database_sync_to_async
#     def get_timestamp(self):
#         import datetime
#         return datetime.datetime.now().strftime("%d-%m-%Y %H:%M")