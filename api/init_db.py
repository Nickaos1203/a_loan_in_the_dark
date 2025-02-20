from sqlmodel import SQLModel, Session, create_engine, select
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings
import argparse

def init_db(username: str, email: str, password: str):
    engine = create_engine(settings.DATABASE_URL)
    
    # Créer toutes les tables
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Vérifier si un conseiller existe déjà
        existing_user = session.exec(
            select(User).where(User.role == "CONSEILLER")
        ).first()
        
        if existing_user:
            print("Un conseiller existe déjà dans la base de données.")
            print(f"Username: {existing_user.username}, Email: {existing_user.email}")
            return
        
        # Créer le premier conseiller
        first_advisor = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            role="CONSEILLER",
            is_active=True
        )
        
        try:
            session.add(first_advisor)
            session.commit()
            session.refresh(first_advisor)
            print(f"Conseiller '{username}' créé avec succès!")
            
            # Vérification immédiate
            created_user = session.exec(
                select(User).where(User.username == username)
            ).first()
            if created_user:
                print("Vérification - Conseiller trouvé dans la base de données:")
                print(f"ID: {created_user.id}")
                print(f"Username: {created_user.username}")
                print(f"Email: {created_user.email}")
                print(f"Role: {created_user.role}")
                print(f"Is active: {created_user.is_active}")
            else:
                print("⚠️ Erreur: Le conseiller n'a pas été trouvé après création")
                
        except Exception as e:
            print(f"Erreur lors de la création du conseiller: {e}")
            session.rollback()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialiser le premier conseiller')
    parser.add_argument('--username', required=True, help='Nom d\'utilisateur du conseiller')
    parser.add_argument('--email', required=True, help='Email du conseiller')
    parser.add_argument('--password', required=True, help='Mot de passe du conseiller')
    
    args = parser.parse_args()
    init_db(args.username, args.email, args.password)

    #python init_db.py --username conseiller --email conseiller@mail.com --password MotDePasse123!