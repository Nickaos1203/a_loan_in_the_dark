from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    api_token = models.CharField(max_length=255, null=True, blank=True)
    first_connection = models.BooleanField(default=True)
    profile_picture = models.FilePathField(null=True)
    phone_number = models.CharField(max_length=55, null=True, blank=True)
    advisor =  models.ManyToManyField("self", symmetrical=False)
    password = models.CharField(max_length=128, null=True, blank=True, default="default_password_kiserari1")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'custom_user'

    def __repr__(self):
        return self.email

