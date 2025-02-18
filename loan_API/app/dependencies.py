from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.auth import verify_token  # Fonction de vérification du token
from app.models.user import User  # Ton modèle utilisateur
from sqlalchemy.orm import Session
from app.database import get_db  # Fonction pour obtenir la session de la base de données

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_data = verify_token(token)  # Vérifie le token et récupère les données
        user = db.query(User).filter(User.email == user_data['sub']).first()  # Cherche l'utilisateur dans la DB
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur non trouvé",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
