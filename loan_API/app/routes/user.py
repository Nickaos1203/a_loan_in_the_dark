from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user, get_user_by_id
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/create_user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_new_user(user_create: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Crée un nouvel utilisateur, accessible uniquement pour les utilisateurs staff"""
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès interdit. Vous devez être un utilisateur staff.",
        )
    return create_user(db=db, user_create=user_create)

@router.get("/user/{user_id}", response_model=UserRead)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """Récupère un utilisateur par son ID"""
    return get_user_by_id(db=db, user_id=user_id)

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }