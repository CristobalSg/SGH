import pytest
from fastapi import status


class TestAuthIntegration:
    """Pruebas de integración para la API de autenticación (/auth)"""

    def test_register_user_success(self, client, sample_user_data):
        """Prueba POST /api/auth/register para registrar un usuario exitosamente"""
        response = client.post("/api/auth/register", json=sample_user_data)
        
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
        client.post("/api/auth/register", json=sample_user_data)
        
        # Intentar registrar con el mismo email
        response = client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "El email ya está registrado" in response.json()["detail"]

    def test_register_user_invalid_data(self, client):
        """Prueba POST /auth/register con datos inválidos"""
        invalid_data = {
            "email": "invalid-email",  # Email inválido
            "contrasena": "123",  # Contraseña muy corta
            "nombre": ""  # Nombre vacío
        }
        
        response = client.post("/api/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_missing_fields(self, client):
        """Prueba POST /auth/register con campos faltantes"""
        incomplete_data = {
            "email": "test@example.com"
            # Faltan campos requeridos
        }
        
        response = client.post("/api/auth/register", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_user_success(self, client, sample_user_data):
        """Prueba POST /auth/login con credenciales válidas"""
        # Registrar usuario primero
        client.post("/api/auth/register", json=sample_user_data)
        
        # Hacer login
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["access_token"] is not None

    def test_login_user_invalid_credentials(self, client, sample_user_data):
        """Prueba POST /auth/login con credenciales inválidas"""
        # Registrar usuario primero
        client.post("/api/auth/register", json=sample_user_data)
        
        # Intentar login con contraseña incorrecta
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": "wrong_password"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email o contraseña incorrectos" in response.json()["detail"]

    def test_login_user_nonexistent(self, client):
        """Prueba POST /auth/login con usuario que no existe"""
        login_data = {
            "email": "nonexistent@example.com",
            "contrasena": "password123"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email o contraseña incorrectos" in response.json()["detail"]

    def test_login_json_success(self, client, sample_user_data):
        """Prueba POST /auth/login-json con credenciales válidas"""
        # Registrar usuario primero
        client.post("/api/auth/register", json=sample_user_data)
        
        # Hacer login usando endpoint JSON
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        response = client.post("/api/auth/login-json", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_get_current_user_success(self, client, sample_user_data):
        """Prueba GET /auth/me con token válido"""
        # Registrar usuario
        register_response = client.post("/api/auth/register", json=sample_user_data)
        user_data = register_response.json()
        
        # Hacer login para obtener token
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Obtener información del usuario actual
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_data["id"]
        assert data["email"] == sample_user_data["email"]
        assert data["nombre"] == sample_user_data["nombre"]

    def test_get_current_user_no_token(self, client):
        """Prueba GET /auth/me sin token"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token de autorización requerido" in response.json()["detail"]

    def test_get_current_user_invalid_token(self, client):
        """Prueba GET /auth/me con token inválido"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_malformed_authorization(self, client):
        """Prueba GET /auth/me con header de autorización mal formado"""
        headers = {"Authorization": "InvalidFormat token123"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token debe ser de tipo Bearer" in response.json()["detail"]

    def test_login_missing_fields(self, client):
        """Prueba POST /auth/login con campos faltantes"""
        incomplete_data = {
            "email": "test@example.com"
            # Falta contrasena
        }
        
        response = client.post("/api/auth/login", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_detailed_user_info_success(self, client, sample_user_data):
        """Prueba GET /auth/me/detailed con token válido"""
        # Registrar usuario
        register_response = client.post("/api/auth/register", json=sample_user_data)
        
        # Hacer login para obtener token
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Obtener información detallada del usuario
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me/detailed", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "user_id" in data
        assert "email" in data
        assert "nombre" in data
        assert "rol" in data
        assert "activo" in data
        assert data["email"] == sample_user_data["email"]

    def test_get_detailed_user_info_no_token(self, client):
        """Prueba GET /auth/me/detailed sin token"""
        response = client.get("/api/auth/me/detailed")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token de autorización requerido" in response.json()["detail"]

    def test_refresh_token_success(self, client, sample_user_data):
        """Prueba POST /auth/refresh con refresh token válido"""
        # Registrar usuario
        client.post("/api/auth/register", json=sample_user_data)
        
        # Hacer login para obtener tokens
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        login_data_response = login_response.json()
        
        # Verificar que se incluye refresh_token
        assert "refresh_token" in login_data_response
        refresh_token = login_data_response["refresh_token"]
        
        # Usar refresh token para obtener nuevo access token
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/auth/refresh", json=refresh_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_refresh_token_invalid(self, client):
        """Prueba POST /auth/refresh con refresh token inválido"""
        refresh_data = {"refresh_token": "invalid_refresh_token"}
        response = client.post("/api/auth/refresh", json=refresh_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token de refresh inválido" in response.json()["detail"]

    def test_validate_role_success(self, client, sample_admin_user_data):
        """Prueba GET /auth/validate-role/{role} con rol válido"""
        # Registrar usuario administrador
        client.post("/api/auth/register", json=sample_admin_user_data)
        
        # Hacer login
        login_data = {
            "email": sample_admin_user_data["email"],
            "contrasena": sample_admin_user_data["contrasena"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Validar rol administrador
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/validate-role/administrador", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is True
        assert data["user_rol"] == "administrador"
        assert data["required_role"] == "administrador"

    def test_validate_role_invalid(self, client, sample_user_data):
        """Prueba GET /auth/validate-role/{role} con rol inválido"""
        # Registrar usuario normal (docente por defecto)
        client.post("/api/auth/register", json=sample_user_data)
        
        # Hacer login
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Intentar validar rol administrador (debería fallar)
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/validate-role/administrador", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is False
        assert data["user_rol"] == "docente"  # o el rol por defecto que tengas
        assert data["required_role"] == "administrador"

    def test_validate_role_no_token(self, client):
        """Prueba GET /auth/validate-role/{role} sin token"""
        response = client.get("/api/auth/validate-role/administrador")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_response_includes_only_token(self, client, sample_user_data):
        """Prueba que la respuesta de login incluya solo información del token"""
        # Registrar usuario
        client.post("/api/auth/register", json=sample_user_data)
        
        # Hacer login
        login_data = {
            "email": sample_user_data["email"],
            "contrasena": sample_user_data["contrasena"]
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        
        # Verificar que NO se incluya información del usuario ni rol en la respuesta
        assert "user" not in data
        assert "rol" not in data
        
        # Verificar que el token type sea bearer
        assert data["token_type"] == "bearer"

    def test_register_with_different_roles(self, client):
        """Prueba registro de usuarios con diferentes roles"""
        roles_data = [
            {
                "email": "docente@test.com",
                "contrasena": "Password123!",
                "nombre": "Juan",
                "rol": "docente"
            },
            {
                "email": "estudiante@test.com",
                "contrasena": "Password123!",
                "nombre": "María",
                "rol": "estudiante"
            },
            {
                "email": "admin@test.com",
                "contrasena": "Password123!",
                "nombre": "Admin",
                "rol": "administrador"
            }
        ]
        
        for user_data in roles_data:
            response = client.post("/api/auth/register", json=user_data)
            assert response.status_code == status.HTTP_201_CREATED
            
            data = response.json()
            assert data["rol"] == user_data["rol"]
            assert data["email"] == user_data["email"]
            assert data["nombre"] == user_data["nombre"]