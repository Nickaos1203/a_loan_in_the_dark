import requests
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)

class APIClient:
    @staticmethod
    def login(email, password):
        # Simuler une connexion réussie
        return {"access_token": "debug_token"}

    @staticmethod
    def get_user_info(token):
        # Retourner des infos statiques
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(email="leo@staff.fr")
            return {
                "id": str(user.id),
                "email": user.email,
                "is_staff": user.is_staff,
                "first_connection": False
            }
        except Exception:
            return {
                "id": "debug_user_id",
                "email": "leo@staff.fr",
                "is_staff": True,
                "first_connection": False
            }

    @staticmethod
    def update_password(token, new_password):
        # Simuler une mise à jour de mot de passe réussie
        return {"message": "Mot de passe mis à jour avec succès"}