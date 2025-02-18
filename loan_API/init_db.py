from app.database import engine, Session
from app.models.user import User
from app.services.user import create_user
from app.schemas.user import UserCreate

# Liste des utilisateurs à créer
users_data = [
    {"email": "vic@staff.fr", "password": "password1234", "is_staff": True},
    {"email": "nico@staff.fr", "password": "password1234", "is_staff": True},
    {"email": "leo@staff.fr", "password": "password1234", "is_staff": True},
]


def init_db():
    """Initialise la base de données avec des utilisateurs par défaut"""
    with Session(engine) as session:
        for user in users_data:
            user_create = UserCreate(email=user["email"],password=user["password"],is_staff=user["is_staff"])
            create_user(db=session, user_create=user_create)
        print("utilisateurs staffs importés avec succés")
# Exécuter la fonction si ce fichier est lancé directement
if __name__ == "__main__":
    init_db()
