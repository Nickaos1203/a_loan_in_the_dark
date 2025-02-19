import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.user import User
from app.services.user import create_user
from app.schemas.user import UserCreate
from app.database import get_db
from sqlmodel import SQLModel

TEST_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

super_user = {
  "email": "superuser@email.com",
  "password": "password1234",
  "is_staff": True
}

staff_user = {
  "email": "staff@email.com",
  "password": "password1234",
  "is_staff": True
}

@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    db = TestingSessionLocal()  # Utiliser la base de test
    db.commit()

    # 1. Créer le super utilisateur
    super_user_data = UserCreate(**super_user)
    create_user(db, super_user_data)
    db.commit()  # Sauvegarde en base

    # 2. Obtenir un token en se connectant avec le super utilisateur
    response = client.post("/auth/login", json={"email": super_user["email"], "password": super_user["password"]})
    print("Response status:", response.status_code)
    print("Response body:", response.json())

    token = response.json().get("access_token")
    return token

def test_create_staff_user(setup_db):
    """Teste la création d'un utilisateur staff avec un super user authentifié"""

    token = setup_db  # Récupère le token depuis la fixture

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/users", json=staff_user, headers=headers)

    assert response.status_code == 201
    assert response.json()["email"] == "staff@email.com"