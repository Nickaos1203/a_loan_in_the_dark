from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from accounts.utils import generate_profile_picture

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    api_token = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='accounts', null=True, blank=True)
    phone_number = models.CharField(max_length=55, null=True, blank=True)
    advisor =  models.ManyToManyField("self", symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'custom_user'

    def __repr__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.profile_picture:  # Vérifie si l'utilisateur n'a pas encore d'image
            first_letter = self.email[0].upper() if self.email else "U"
            self.profile_picture = generate_profile_picture(first_letter)
        
        super().save(*args, **kwargs)

