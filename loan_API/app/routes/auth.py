from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserConnection
from app.services.auth import create_access_token
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/login")
def login(user: UserConnection,db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Cet utilisateur n'est pas enregistré")
    elif not db_user.verify_password(user.password):  
        raise HTTPException(status_code=401, detail="mauvais mdp")
    else:
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
