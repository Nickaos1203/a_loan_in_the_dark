from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_chats')
    advisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='advisor_chats')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
