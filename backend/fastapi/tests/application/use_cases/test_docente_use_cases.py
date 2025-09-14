import pytest
from unittest.mock import Mock, create_autospec
from fastapi import HTTPException, status
from typing import List

# Importaciones del sistema bajo prueba
from application.use_cases.docente_use_cases import DocenteUseCases
from infrastructure.repositories.docente_repository import DocenteRepository
from domain.entities import Docente, DocenteCreate


class TestDocenteUseCases:
    """Pruebas unitarias para el caso de uso DocenteUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(DocenteRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_cases = DocenteUseCases(self.mock_repo)

    def test_get_all_returns_all_docentes(self):
        """Prueba que get_all retorna todos los docentes del repositorio"""
        # Arrange
        expected_docentes = [
            Docente(
                id=1,
                nombre="Juan",
                apellido="Pérez",
                email="juan.perez@example.com",
                contrasena="password123"
            ),
            Docente(
                id=2,
                nombre="María",
                apellido="González",
                email="maria.gonzalez@example.com",
                telefono="987654321"
            )
        ]
        self.mock_repo.get_all.return_value = expected_docentes

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == expected_docentes
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_by_id_returns_docente_when_exists(self):
        """Prueba que get_by_id retorna el docente cuando existe"""
        # Arrange
        docente_id = 1
        expected_docente = Docente(
            id=docente_id,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            contrasena="password123"
        )
        self.mock_repo.get_by_id.return_value = expected_docente

        # Act
        result = self.use_cases.get_by_id(docente_id)

        # Assert
        assert result == expected_docente
        self.mock_repo.get_by_id.assert_called_once_with(docente_id)

    def test_get_by_id_raises_exception_when_not_exists(self):
        """Prueba que get_by_id lanza excepción cuando el docente no existe"""
        # Arrange
        docente_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_id(docente_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Docente no encontrado" in str(exc_info.value.detail)

    def test_create_docente_success(self):
        """Prueba creación exitosa de docente"""
        # Arrange
        docente_data = DocenteCreate(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            contrasena="password123"
        )
        expected_docente = Docente(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            contrasena="password123"
        )
        self.mock_repo.get_by_email.return_value = None  # Email no existe
        self.mock_repo.create.return_value = expected_docente

        # Act
        result = self.use_cases.create(docente_data)

        # Assert
        assert result == expected_docente
        self.mock_repo.get_by_email.assert_called_once_with("juan.perez@example.com")
        self.mock_repo.create.assert_called_once_with(docente_data)

    def test_create_docente_email_already_exists(self):
        """Prueba creación de docente con email que ya existe"""
        # Arrange
        docente_data = DocenteCreate(
            nombre="Juan",
            apellido="Pérez",
            email="existing@example.com",
            contrasena="password123"
        )
        existing_docente = Docente(
            id=1,
            nombre="Existing",
            apellido="Docente",
            email="existing@example.com",
            telefono="111111111"
        )
        self.mock_repo.get_by_email.return_value = existing_docente

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.create(docente_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "El email ya está registrado" in str(exc_info.value.detail)

    def test_update_docente_success(self):
        """Prueba actualización exitosa de docente"""
        # Arrange
        docente_id = 1
        update_data = {"nombre": "Juan Carlos", "telefono": "999888777"}
        existing_docente = Docente(
            id=docente_id,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            contrasena="password123"
        )
        updated_docente = Docente(
            id=docente_id,
            nombre="Juan Carlos",
            apellido="Pérez",
            email="juan.perez@example.com",
            telefono="999888777"
        )
        
        self.mock_repo.get_by_id.return_value = existing_docente
        self.mock_repo.update.return_value = updated_docente

        # Act
        result = self.use_cases.update(docente_id, **update_data)

        # Assert
        assert result == updated_docente
        self.mock_repo.get_by_id.assert_called_once_with(docente_id)
        self.mock_repo.update.assert_called_once_with(docente_id, update_data)

    def test_delete_docente_success(self):
        """Prueba eliminación exitosa de docente"""
        # Arrange
        docente_id = 1
        existing_docente = Docente(
            id=docente_id,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            contrasena="password123"
        )
        
        self.mock_repo.get_by_id.return_value = existing_docente
        self.mock_repo.delete.return_value = True

        # Act
        result = self.use_cases.delete(docente_id)

        # Assert
        assert result is True
        self.mock_repo.get_by_id.assert_called_once_with(docente_id)
        self.mock_repo.delete.assert_called_once_with(docente_id)