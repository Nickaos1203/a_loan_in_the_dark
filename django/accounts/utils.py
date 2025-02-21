import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class APIClient:
    @staticmethod
    def login(username, password):
        try:
            url = f"{settings.API_BASE_URL}/auth/token"
            print(f"Tentative de connexion à : {url}")
            
            data = {
                "username": username,
                "password": password
            }
            print(f"Data envoyée : {data}")
            
            response = requests.post(url, data=data)
            print(f"Status code : {response.status_code}")
            print(f"Réponse : {response.text}")
            
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"Erreur lors de la connexion : {str(e)}")
            return None

    @staticmethod
    def get_user_info(token):
        try:
            url = f"{settings.API_BASE_URL}/users/me"
            print(f"URL complète pour get_user_info : {url}")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            print(f"Headers : {headers}")
            
            response = requests.get(url, headers=headers)
            print(f"Status code : {response.status_code}")
            print(f"Response body : {response.text}")
            
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"Exception dans get_user_info : {str(e)}")
            return None