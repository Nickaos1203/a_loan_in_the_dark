from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import auth, users
from app.db.session import engine
from sqlmodel import SQLModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI()

# Modification des préfixes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])  # Changement ici