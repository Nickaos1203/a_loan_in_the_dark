from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('CONSEILLER', 'Conseiller'),
        ('CLIENT', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
    api_token = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'custom_user'