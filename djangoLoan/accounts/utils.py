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
            headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
            data = {
            "email": email,
            "password": password
            }
        
            response = requests.post(
            url, 
            headers=headers,
            json=data  
        )
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
        
@staticmethod
def list_users(token):
        try:
            url = f"{settings.API_BASE_URL}/list"
            headers = {
                'Authorization': f"Bearer {token}",
                'Accept': 'application/json'
            }
            response = requests.get(url, headers=headers)
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"Error listing users: {str(e)}")
            return None

@staticmethod
def create_user(token, user_data):
        try:
            url = f"{settings.API_BASE_URL}/create_user"
            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(url, headers=headers, json=user_data)
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

@staticmethod
def delete_user(token, user_id):
        try:
            url = f"{settings.API_BASE_URL}/user/{user_id}"
            headers = {
                'Authorization': f"Bearer {token}",
                'Accept': 'application/json'
            }
            response = requests.delete(url, headers=headers)
            return response.ok
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False