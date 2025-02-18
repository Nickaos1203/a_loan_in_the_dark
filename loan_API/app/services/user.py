from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate) -> UserRead:
    """Crée un utilisateur avec un mot de passe hashé et le sauvegarde dans la base de données"""
    # Vérifie si l'email existe déjà
    db_user = db.query(User).filter(User.email == user_create.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé",
        )
    
    # Crée un nouvel utilisateur
    hashed_password = pwd_context.hash(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        is_staff=False,  # Par défaut, un nouvel utilisateur n'est pas staff
        is_active=True,  # Par défaut, l'utilisateur est actif
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Retourne l'utilisateur créé (sans le mot de passe)
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        is_staff=db_user.is_staff,
        is_active=db_user.is_active,
        profile_picture=db_user.profile_picture,
    )

def get_user_by_id(db: Session, user_id: UUID) -> UserRead:
    """Récupère un utilisateur par son ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )
    
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        is_staff=db_user.is_staff,
        is_active=db_user.is_active,
        profile_picture=db_user.profile_picture,
    )
