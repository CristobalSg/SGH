import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from infrastructure.database.config import get_db, Base

# Base de datos en memoria para las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Crear engine para pruebas
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False  # Cambiar a True para debug SQL
)

# Configurar foreign keys para SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dependencia get_db para usar base de datos de prueba"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def db_session():
    """Fixture que proporciona una sesión de base de datos para las pruebas"""
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpiar todas las tablas después de cada prueba
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Fixture que proporciona un cliente de prueba para FastAPI"""
    # Override de la dependencia de base de datos
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar overrides después de la prueba
    app.dependency_overrides.clear()


@pytest.fixture
def sample_docente_data():
    """Datos de muestra para crear un docente"""
    return {
        "nombre": "Juan Pérez",
        "email": "juan.perez@universidad.edu",
        "pass_hash": "hashed_password_123"
    }


@pytest.fixture
def sample_restriccion_data():
    """Datos de muestra para crear una restricción"""
    return {
        "docente_id": 1,
        "tipo": "horario",
        "valor": "08:00-12:00",
        "prioridad": 5,
        "restriccion_blanda": "Preferible mañanas",
        "restriccion_dura": "No disponible tardes"
    }


@pytest.fixture
def sample_restriccion_update_data():
    """Datos de muestra para actualizar una restricción"""
    return {
        "tipo": "aula",
        "valor": "Laboratorio A",
        "prioridad": 8,
        "restriccion_blanda": "Preferible laboratorio",
        "restriccion_dura": "Solo laboratorios"
    }


@pytest.fixture
def sample_restriccion_patch_data():
    """Datos de muestra para actualización parcial de una restricción"""
    return {
        "prioridad": 9,
        "restriccion_blanda": "Alta prioridad"
    }
