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

TEST_DATABASE_URL = "sqlite:///./app/tests/test.db"
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

basic_user = {
  "email": "email@email.com",
  "password": "password1234",
  "is_staff": False
}

basic_user2 = {
  "email": "email2@email.com",
  "password": "password1234",
  "is_staff": False
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
    response = client.post("/create_user", json=staff_user, headers=headers)

    assert response.status_code == 201
    assert response.json()["email"] == "staff@email.com"

    response = client.post("/create_user", json=staff_user, headers=headers)
    assert response.status_code == 400  # Utilisateur déja créé

def test_create_basic_user(setup_db):
    """Teste la création d'un utilisateur non staff avec un super user authentifié"""

    token = setup_db  # Récupère le token depuis la fixture

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/create_user", json=basic_user, headers=headers)

    assert response.status_code == 201
    assert response.json()["email"] == "email@email.com"

    response = client.post("/create_user", json=basic_user, headers=headers)
    assert response.status_code == 400  # Utilisateur déja créé

def test_basic_user():
  body = {
  "email": "email@email.com",
  "password": "password1234"
  }
  response = client.post("auth/login", json=body)
  assert response.status_code == 200

  token = response.json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}
  response = client.get("/me", headers=headers)
  assert response.status_code == 200
  assert response.json()["email"] == "email@email.com"

  response = client.post("/create_user", headers=headers, json=staff_user)
  assert response.status_code == 403

def test_staff_user():
  body = {
  "email": "staff@email.com",
  "password": "password1234"
  }
  response = client.post("auth/login", json=body)
  assert response.status_code == 200

  token = response.json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}
  response = client.get("/me", headers=headers)
  assert response.status_code == 200
  assert response.json()["email"] == "staff@email.com"

  response = client.post("/create_user", headers=headers, json=basic_user2)
  assert response.status_code == 201
  assert response.json()["email"] == "email2@email.com"
  id_user = response.json()["id"]

  url = "/user/" + id_user
  response = client.get(url, headers=headers)
  assert response.status_code == 200
  assert response.json()["email"] == "email2@email.com"

def test_create_loan():
  body = {
  "email": "staff@email.com",
  "password": "password1234"
  }
  response = client.post("auth/login", json=body)
  assert response.status_code == 200    

  body= {"state" : "OH",
        "bank" : "CAPITAL ONE NATL ASSOC",
        "naics" : "54",
        "term" : 60,
        "no_emp" : 13,
        "new_exist" : 1,
        "create_job" : 0,
        "retained_job":3,
        "urban_rural":1,
        "rev_line_cr":"N",
        "low_doc":"N",
        "gr_appv":50000,
        "recession":0,
        "has_franchise":1,
        "user_email":"email@email.com"
        }
  
  body["state"] = None
  response = client.post("loans/create_loan/", json=body)
  assert response.status_code == 422 
