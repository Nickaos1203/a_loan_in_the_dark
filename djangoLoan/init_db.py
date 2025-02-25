
import json
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoApp.settings')  
django.setup()  
from accounts.models import CustomUser


def init_django_db():
    with open('users_data.json', 'r') as file:
        users_data = json.load(file)
    for user in users_data:
        # Vérifier si l'utilisateur existe déjà pour éviter les doublons
        if not CustomUser.objects.filter(email=user["email"]).exists():
            new_user = CustomUser(
                id=user["id"],  # Assurez-vous que l'ID est unique ou laissé vide pour qu'il soit généré automatiquement
                email=user["email"],
                is_staff=user["is_staff"],
                password = None
            )
            # new_user.set_password("password1234")  # Utiliser set_password pour hacher le mot de passe
            new_user.save()
            print(f"Utilisateur {user['email']} créé avec succès.")
        else:
            print(f"L'utilisateur {user['email']} existe déjà.")




# Exécuter la fonction si ce fichier est lancé directement
if __name__ == "__main__":
    init_django_db()



