import pytest
from fastapi import status


class TestAuthIntegration:
    """Pruebas de integración para la API de autenticación (/auth)"""

    def test_register_user_success(self, client, sample_user_data):
        """Prueba POST /auth/register para registrar un usuario exitosamente"""
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["nombre"] == sample_user_data["nombre"]
        assert data["apellido"] == sample_user_data["apellido"]
        assert data["is_active"] is True
        assert "id" in data
        # La contraseña no debe estar en la respuesta
        assert "contrasena" not in data

    def test_register_user_duplicate_email(self, client, sample_user_data):
        """Prueba POST /auth/register con email duplicado"""
        # Registrar usuario por primera vez
        client.post("/auth/register", json=sample_user_data)
        
        # Intentar registrar con el mismo email
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "El email ya está registrado" in response.json()["detail"]

    def test_register_user_invalid_data(self, client):
        """Prueba POST /auth/register con datos inválidos"""
        invalid_data = {
            "email": "invalid-email",  # Email inválido
            "contrasena": "123",  # Contraseña muy corta
            "nombre": ""  # Nombre vacío
        }
        
        response = client.post("/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_missing_fields(self, client):
        """Prueba POST /auth/register con campos faltantes"""
        incomplete_data = {
            "email": "test@example.com"
            # Faltan campos requeridos
        }
        
        response = client.post("/auth/register", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_user_success(self, client, sample_user_data):
        """Prueba POST /auth/login con credenciales válidas"""
        # Registrar usuario primero
        client.post("/auth/register", json=sample_user_data)
        
        # Hacer login
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["access_token"] is not None

    def test_login_user_invalid_credentials(self, client, sample_user_data):
        """Prueba POST /auth/login con credenciales inválidas"""
        # Registrar usuario primero
        client.post("/auth/register", json=sample_user_data)
        
        # Intentar login con contraseña incorrecta
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": "wrong_password"
        }
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email o contraseña incorrectos" in response.json()["detail"]

    def test_login_user_nonexistent(self, client):
        """Prueba POST /auth/login con usuario que no existe"""
        login_data = {
            "email": "nonexistent@example.com",
            "contrasena": "password123"
        }
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email o contraseña incorrectos" in response.json()["detail"]

    def test_login_json_success(self, client, sample_user_data):
        """Prueba POST /auth/login-json con credenciales válidas"""
        # Registrar usuario primero
        client.post("/auth/register", json=sample_user_data)
        
        # Hacer login usando endpoint JSON
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        response = client.post("/auth/login-json", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_get_current_user_success(self, client, sample_user_data):
        """Prueba GET /auth/me con token válido"""
        # Registrar usuario
        register_response = client.post("/auth/register", json=sample_user_data)
        user_data = register_response.json()
        
        # Hacer login para obtener token
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        login_response = client.post("/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Obtener información del usuario actual
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_data["id"]
        assert data["email"] == sample_user_data["email"]
        assert data["nombre"] == sample_user_data["nombre"]

    def test_get_current_user_no_token(self, client):
        """Prueba GET /auth/me sin token"""
        response = client.get("/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token de autorización requerido" in response.json()["detail"]

    def test_get_current_user_invalid_token(self, client):
        """Prueba GET /auth/me con token inválido"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_malformed_authorization(self, client):
        """Prueba GET /auth/me con header de autorización mal formado"""
        headers = {"Authorization": "InvalidFormat token123"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token debe ser de tipo Bearer" in response.json()["detail"]

    def test_login_missing_fields(self, client):
        """Prueba POST /auth/login con campos faltantes"""
        incomplete_data = {
            "email": "test@example.com"
            # Falta contrasena
        }
        
        response = client.post("/auth/login", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY