import pytest
from unittest.mock import Mock, create_autospec
from fastapi import HTTPException, status
from typing import List

# Importaciones del sistema bajo prueba
from application.use_cases.seccion_use_cases import SeccionUseCases
from infrastructure.repositories.seccion_repository import SeccionRepository
from domain.entities import Seccion, SeccionCreate


class TestSeccionUseCases:
    """Pruebas unitarias para el caso de uso SeccionUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(SeccionRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_cases = SeccionUseCases(self.mock_repo)

    def test_get_all_returns_all_secciones(self):
        """Prueba que get_all retorna todas las secciones del repositorio"""
        # Arrange
        expected_secciones = [
            Seccion(
                id=1,
                codigo="SEC-001",
                anio=2024,
                semestre=1,
                cupos=30,
                asignatura_id=1,
                docente_id=1,
                periodo="2024-1"
            ),
            Seccion(
                id=2,
                codigo="SEC-002",
                anio=2024,
                semestre=1,
                cupos=25,
                asignatura_id=1,
                docente_id=2,
                periodo="2024-1"
            )
        ]
        self.mock_repo.get_all.return_value = expected_secciones

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == expected_secciones
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_by_id_returns_seccion_when_exists(self):
        """Prueba que get_by_id retorna la sección cuando existe"""
        # Arrange
        seccion_id = 1
        expected_seccion = Seccion(
            id=seccion_id,
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=30,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-1"
        )
        self.mock_repo.get_by_id.return_value = expected_seccion

        # Act
        result = self.use_cases.get_by_id(seccion_id)

        # Assert
        assert result == expected_seccion
        self.mock_repo.get_by_id.assert_called_once_with(seccion_id)

    def test_get_by_id_raises_exception_when_not_exists(self):
        """Prueba que get_by_id lanza excepción cuando la sección no existe"""
        # Arrange
        seccion_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_id(seccion_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Sección no encontrada" in str(exc_info.value.detail)

    def test_create_seccion_success(self):
        """Prueba creación exitosa de sección"""
        # Arrange
        seccion_data = SeccionCreate(
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=30,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-1"
        )
        expected_seccion = Seccion(
            id=1,
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=30,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-1"
        )
        self.mock_repo.get_by_codigo.return_value = None  # Código no existe
        self.mock_repo.create.return_value = expected_seccion

        # Act
        result = self.use_cases.create(seccion_data)

        # Assert
        assert result == expected_seccion
        self.mock_repo.get_by_codigo.assert_called_once_with("SEC-001")
        self.mock_repo.create.assert_called_once_with(seccion_data)

    def test_create_seccion_already_exists(self):
        """Prueba creación de sección con código que ya existe"""
        # Arrange
        seccion_data = SeccionCreate(
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=30,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-1"
        )
        existing_seccion = Seccion(
            id=1,
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=30,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-1"
        )
        self.mock_repo.get_by_codigo.return_value = existing_seccion

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.create(seccion_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe una sección con ese código" in str(exc_info.value.detail)

    def test_update_seccion_success(self):
        """Prueba actualización exitosa de sección"""
        # Arrange
        seccion_id = 1
        update_data = {"cupos": 35, "periodo": "2024-2"}
        existing_seccion = Seccion(
            id=seccion_id,
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=30,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-1"
        )
        updated_seccion = Seccion(
            id=seccion_id,
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=35,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-2"
        )
        
        self.mock_repo.get_by_id.return_value = existing_seccion
        self.mock_repo.update.return_value = updated_seccion

        # Act
        result = self.use_cases.update(seccion_id, **update_data)

        # Assert
        assert result == updated_seccion
        self.mock_repo.get_by_id.assert_called_once_with(seccion_id)
        self.mock_repo.update.assert_called_once_with(seccion_id, update_data)

    def test_delete_seccion_success(self):
        """Prueba eliminación exitosa de sección"""
        # Arrange
        seccion_id = 1
        existing_seccion = Seccion(
            id=seccion_id,
            codigo="SEC-001",
            anio=2024,
            semestre=1,
            cupos=30,
            asignatura_id=1,
            docente_id=1,
            periodo="2024-1"
        )
        
        self.mock_repo.get_by_id.return_value = existing_seccion
        self.mock_repo.tiene_clases.return_value = False  # No tiene clases asociadas
        self.mock_repo.delete.return_value = True

        # Act
        result = self.use_cases.delete(seccion_id)

        # Assert
        assert result is True
        self.mock_repo.get_by_id.assert_called_once_with(seccion_id)
        self.mock_repo.tiene_clases.assert_called_once_with(seccion_id)
        self.mock_repo.delete.assert_called_once_with(seccion_id)