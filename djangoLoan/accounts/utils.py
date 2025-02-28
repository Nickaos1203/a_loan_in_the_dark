import requests
from django.conf import settings
import logging
import json
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO

logger = logging.getLogger(__name__)

class APIClient:
    @staticmethod
    def login(email, password):
        try:
            url = f"{settings.API_BASE_URL}/auth/login"
            
            data = {
                "email": email,
                "password": password
            }
            data_json = json.dumps(data)
            headers = {
                "Accept": "application/json"
            }
            response = requests.post(url, data=data_json, headers=headers)
            
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
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"Exception dans get_user_info : {str(e)}")
            return None

    @staticmethod
    def update_password(token, new_password):
        """
        Met à jour le mot de passe d'un utilisateur via l'API.
        
        :param token: Token d'authentification de l'utilisateur.
        :param new_password: Nouveau mot de passe à définir.
        :return: Dictionnaire contenant la réponse de l'API ou None en cas d'erreur.
        """
        try:
            url = f"{settings.API_BASE_URL}/update-password"
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            new_password = str(new_password)
            data = json.dumps({"new_password": new_password})
            
            response = requests.put(url, data=data, headers=headers)

            if response.ok:
                return response.json()
            else:
                return {"error": f"Échec de la mise à jour : {response.text}"}
        except Exception as e:
            print(f"Erreur dans update_password : {str(e)}")
            return {"error": str(e)}

def generate_profile_picture(letter):
    """Génère une image avec la première lettre de l'email."""
    img_size = (100, 100)  # Taille de l'image
    background_color = (0, 123, 255)  # Bleu par défaut
    text_color = (255, 255, 255)  # Blanc
    
    # Création de l'image
    img = Image.new('RGB', img_size, background_color)
    draw = ImageDraw.Draw(img)

    # Chargement d'une police de caractères (optionnel, sinon utilise la police par défaut)
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        font = ImageFont.load_default()

    # Taille du texte
    text_size = draw.textbbox((0, 0), letter, font=font)
    text_x = (img_size[0] - text_size[2]) / 2
    text_y = (img_size[1] - text_size[3]) / 2

    # Dessiner la lettre
    draw.text((text_x, text_y), letter, fill=text_color, font=font)

    # Sauvegarde en mémoire
    img_io = BytesIO()
    img.save(img_io, format='PNG')

    return ContentFile(img_io.getvalue(), name=f"default_{letter}.png")
