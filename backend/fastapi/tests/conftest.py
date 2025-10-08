import os
import sys
from pathlib import Path

# Configurar variables de entorno para testing
os.environ.setdefault("NODE_ENV", "testing")
os.environ.setdefault("DB_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test_secret_key_for_testing")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_EXPIRE_MINUTES", "30")

# Añadir el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from domain.models import Base
from infrastructure.database.config import get_db
from domain.entities import UserCreate

# Base de datos en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Importar todos los modelos para asegurar que estén registrados
    from domain.models import (
        Base, User, Docente, Estudiante, Administrador, Campus, Edificio, 
        RestriccionHorario, Asignatura, Seccion, Sala, Bloque, Clase, 
        Restriccion
    )
    
    # Crear todas las tablas con la estructura actual
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Asegurar que todas las tablas estén creadas
    from domain.models import Base
    Base.metadata.create_all(bind=db_session.bind)
    
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def admin_user_data():
    return UserCreate(
        nombre="Admin Test",
        email="admin@test.com",
        contrasena="Admin123!",
        rol="administrador"
    )

@pytest.fixture
def docente_user_data():
    return UserCreate(
        nombre="Docente Test",
        email="docente@test.com",
        contrasena="Docente123!",
        rol="docente"
    )

@pytest.fixture
def estudiante_user_data():
    return UserCreate(
        nombre="Estudiante Test",
        email="estudiante@test.com",
        contrasena="Estudiante123!",
        rol="estudiante"
    )

@pytest.fixture
def admin_token(client, admin_user_data):
    client.post("/api/auth/register", json=admin_user_data.model_dump())
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": admin_user_data.email,
            "contrasena": admin_user_data.contrasena
        }
    )
    return login_response.json()["access_token"]

@pytest.fixture
def docente_token(client, docente_user_data):
    client.post("/api/auth/register", json=docente_user_data.model_dump())
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": docente_user_data.email,
            "contrasena": docente_user_data.contrasena
        }
    )
    return login_response.json()["access_token"]

@pytest.fixture
def estudiante_token(client, estudiante_user_data):
    client.post("/api/auth/register", json=estudiante_user_data.model_dump())
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": estudiante_user_data.email,
            "contrasena": estudiante_user_data.contrasena
        }
    )
    return login_response.json()["access_token"]

@pytest.fixture
def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture
def auth_headers_docente(docente_token):
    return {"Authorization": f"Bearer {docente_token}"}

@pytest.fixture
def auth_headers_estudiante(estudiante_token):
    return {"Authorization": f"Bearer {estudiante_token}"}

@pytest.fixture
def docente_completo(client, auth_headers_admin):
    """Crea un usuario docente y su registro en la tabla Docente"""
    # Primero crear el usuario con rol docente
    user_data = {
        "nombre": "Carlos Ramírez Docente",
        "email": "docente.completo@test.com",
        "contrasena": "Docente123!",
        "rol": "docente"
    }
    
    # Registrar el usuario
    user_response = client.post("/api/auth/register", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]
    
    # Ahora crear el perfil de docente asociado al usuario
    docente_data = {
        "user_id": user_id,
        "departamento": "Ingeniería"
    }
    
    # Crear el docente
    docente_response = client.post("/api/docentes/", json=docente_data, headers=auth_headers_admin)
    assert docente_response.status_code == 201
    docente_id = docente_response.json()["id"]
    
    # Retornar tanto el user_id como el id del docente
    return {
        "user_id": user_id,
        "docente_id": docente_id,
        "email": user_data["email"],
        "password": user_data["contrasena"]
    }

@pytest.fixture
def auth_headers_docente_completo(client, docente_completo):
    """Headers de autenticación para el docente completo"""
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": docente_completo["email"],
            "contrasena": docente_completo["password"]
        }
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_user(client, admin_user_data):
    """Usuario administrador creado y registrado en la base de datos"""
    response = client.post("/api/auth/register", json=admin_user_data.model_dump())
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def campus_completo(client, auth_headers_admin):
    """Crea un campus completo para usar en tests"""
    campus_data = {
        "codigo": "CAMPUS-TEST",
        "nombre": "Campus Test",
        "direccion": "Calle Test 123"
    }
    
    response = client.post("/api/campus/", json=campus_data, headers=auth_headers_admin)
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def edificio_completo(client, auth_headers_admin, campus_completo):
    """Crea un edificio completo para usar en tests"""
    edificio_data = {
        "codigo": "EDIF-TEST",
        "nombre": "Edificio Test",
        "campus_id": campus_completo["id"]
    }
    
    response = client.post("/api/edificios/", json=edificio_data, headers=auth_headers_admin)
    assert response.status_code == 201
    return response.json()
