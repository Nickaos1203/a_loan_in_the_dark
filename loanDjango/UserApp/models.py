from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('conseiller', 'Conseiller Bancaire'),
    ]

    surname = models.CharField(max_length=100)  # Nom de famille
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    # Évite le conflit avec auth.User.groups et auth.User.user_permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="userapp_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="userapp_users_permissions",
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
