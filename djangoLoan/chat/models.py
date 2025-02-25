from django.db import models
from accounts.models import CustomUser

class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user.email}: {self.content[:30]}"
    
    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%d-%m-%Y %H:%M")
    
    @property
    def is_staff(self):
        return self.user.is_staff