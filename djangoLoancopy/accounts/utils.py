from wsgiref import headers
import requests
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)

class APIClient:
    @staticmethod
    def login(email, password):
        print("on est là !")
        try:
            url = f"{settings.API_BASE_URL}/auth/login"
            print(f"Tentative de connexion à : {url}")
            
            data = {
                "email": email,
                "password": password
            }
            print(data)
            data_json = json.dumps(data)
            print(f"Data envoyée : {data}")
            
            response = requests.post(
            url,
            headers=headers,
            json=data  # Utilisez json au lieu de data
        )
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"Erreur lors de la connexion : {str(e)}")
            return None

    @staticmethod
    def get_user_info(token):
        try:
            url = f"{settings.API_BASE_URL}/me"
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