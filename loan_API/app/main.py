from fastapi import FastAPI
from app.routes import auth, user
from app.database import engine
from sqlmodel import SQLModel

app = FastAPI(title="Loan API", description="API de gestion des prêts bancaires", version="1.0")

# Inclusion des routes
tags_metadata = [
    {"name": "Auth", "description": "Routes d'authentification"},
    {"name": "Users", "description": "Gestion des utilisateurs"},
    {"name": "Loans", "description": "Gestion des demandes de prêts"},
]

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
# app.include_router(loans.router, prefix="/loans", tags=["Loans"])