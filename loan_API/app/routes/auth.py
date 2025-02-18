from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.services.auth import create_access_token

router = APIRouter()

@router.post("/login")
def login(user: UserCreate):
    # Vérification email & password
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
