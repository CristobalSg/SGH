import pytest
from datetime import timedelta, datetime
from unittest.mock import Mock, create_autospec, patch
from fastapi import HTTPException, status

# Importaciones del sistema bajo prueba
from application.use_cases.user_auth_use_cases import UserAuthUseCase
from infrastructure.repositories.user_repository import SQLUserRepository
from domain.entities import UserCreate, User, UserLogin, Token, TokenData


class TestUserAuthUseCase:
    """Pruebas unitarias para el caso de uso UserAuthUseCase"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(SQLUserRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_case = UserAuthUseCase(self.mock_repo)

    def test_register_user_success(self):
        """Prueba registro exitoso de usuario"""
        # Arrange
        user_data = UserCreate(
            email="test@example.com",
            contrasena="Password123!",
            nombre="Test",
            apellido="User"
        )
        expected_user = User(
            id=1,
            email="test@example.com",
            nombre="Test User",
            is_active=True
        )
        
        self.mock_repo.get_by_email.return_value = None  # Email no existe
        self.mock_repo.create.return_value = expected_user

        # Act
        result = self.use_case.register_user(user_data)

        # Assert
        assert result == expected_user
        self.mock_repo.get_by_email.assert_called_once_with("test@example.com")
        self.mock_repo.create.assert_called_once_with(user_data)

    def test_register_user_email_already_exists(self):
        """Prueba registro con email que ya existe"""
        # Arrange
        user_data = UserCreate(
            email="existing@example.com",
            contrasena="Password123!",
            nombre="Test",
            apellido="User"
        )
        existing_user = User(
            id=1,
            email="existing@example.com",
            nombre="Existing User",
            is_active=True
        )
        
        self.mock_repo.get_by_email.return_value = existing_user

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.register_user(user_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "El email ya está registrado" in str(exc_info.value.detail)
        self.mock_repo.get_by_email.assert_called_once_with("existing@example.com")
        self.mock_repo.create.assert_not_called()

    def test_login_user_success(self):
        """Prueba login exitoso de usuario"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            contrasena="password123"
        )
        user = User(
            id=1,
            email="test@example.com",
            nombre="Test",
            apellido="User",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.mock_repo.authenticate.return_value = user
        self.mock_repo.is_active.return_value = True

        # Act
        with patch("application.use_cases.user_auth_use_cases.AuthService") as mock_auth:
            # Configurar el mock para que retorne strings, no MagicMock
            mock_auth_instance = mock_auth.return_value
            mock_auth_instance.create_access_token.return_value = "fake_access_token"
            mock_auth_instance.create_refresh_token.return_value = "fake_refresh_token"
            # También configurar los métodos estáticos
            mock_auth.create_access_token.return_value = "fake_access_token"
            mock_auth.create_refresh_token.return_value = "fake_refresh_token"
            
            result = self.use_case.login_user(login_data)

        # Assert
        assert isinstance(result, Token)
        assert result.access_token == "fake_access_token"
        assert result.refresh_token == "fake_refresh_token"
        assert result.token_type == "bearer"
        self.mock_repo.authenticate.assert_called_once_with("test@example.com", "password123")
        self.mock_repo.is_active.assert_called_once_with(user)

    def test_login_user_invalid_credentials(self):
        """Prueba login con credenciales inválidas"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            contrasena="wrong_password"
        )
        
        self.mock_repo.authenticate.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.login_user(login_data)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email o contraseña incorrectos" in str(exc_info.value.detail)
        self.mock_repo.authenticate.assert_called_once_with("test@example.com", "wrong_password")
        self.mock_repo.is_active.assert_not_called()

    def test_login_user_inactive_user(self):
        """Prueba login con usuario inactivo"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            contrasena="password123"
        )
        user = User(
            id=1,
            email="test@example.com",
            nombre="Test",
            apellido="User",
            is_active=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.mock_repo.authenticate.return_value = user
        self.mock_repo.is_active.return_value = False

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_case.login_user(login_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Usuario inactivo" in str(exc_info.value.detail)
        self.mock_repo.authenticate.assert_called_once_with("test@example.com", "password123")
        self.mock_repo.is_active.assert_called_once_with(user)

    def test_get_current_active_user_success(self):
        """Prueba obtener usuario actual con token válido"""
        # Arrange
        token = "valid_token"
        expected_user = User(
            id=1,
            email="test@example.com",
            nombre="Test",
            apellido="User",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.mock_repo.get_by_email.return_value = expected_user

        # Act
        with patch("application.use_cases.user_auth_use_cases.AuthService") as mock_auth:
            mock_auth.verify_token.return_value = TokenData(email="test@example.com")
            result = self.use_case.get_current_active_user(token)

        # Assert
        assert result == expected_user
        mock_auth.verify_token.assert_called_once_with(token)
        self.mock_repo.get_by_email.assert_called_once_with("test@example.com")

    def test_get_current_active_user_invalid_token(self):
        """Prueba obtener usuario actual con token inválido"""
        # Arrange
        token = "invalid_token"

        # Act & Assert
        with patch("application.use_cases.user_auth_use_cases.AuthService") as mock_auth:
            mock_auth.verify_token.side_effect = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
            
            with pytest.raises(HTTPException) as exc_info:
                self.use_case.get_current_active_user(token)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_active_user_user_not_found(self):
        """Prueba obtener usuario actual cuando el usuario no existe en BD"""
        # Arrange
        token = "valid_token"
        
        self.mock_repo.get_by_email.return_value = None

        # Act & Assert
        with patch("application.use_cases.user_auth_use_cases.AuthService") as mock_auth:
            mock_auth.verify_token.return_value = TokenData(email="nonexistent@example.com")
            
            with pytest.raises(HTTPException) as exc_info:
                self.use_case.get_current_active_user(token)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "No se pudieron validar las credenciales" in str(exc_info.value.detail)