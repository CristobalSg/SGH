import pytest
from datetime import datetime
from unittest.mock import Mock, create_autospec
from fastapi import HTTPException, status
from typing import List

# Importaciones del sistema bajo prueba
from application.use_cases.restriccion_use_cases import RestriccionUseCases
from infrastructure.repositories.restriccion_repository import RestriccionRepository
from domain.entities import Restriccion, RestriccionCreate


class TestRestriccionUseCases:
    """Pruebas unitarias para el caso de uso RestriccionUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(RestriccionRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_cases = RestriccionUseCases(self.mock_repo)

    def test_get_all_returns_all_restricciones(self):
        """Prueba que get_all retorna todas las restricciones del repositorio"""
        # Arrange
        expected_restricciones = [
            Restriccion(
                id=1,
                docente_id=1,
                tipo="horario",
                valor="08:00-12:00",
                prioridad=5,
                restriccion_blanda="Flexible en horarios",
                restriccion_dura=None,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Restriccion(
                id=2,
                docente_id=1,
                tipo="aula",
                valor="Sala A",
                prioridad=3,
                restriccion_blanda=None,
                restriccion_dura="Obligatorio",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        self.mock_repo.get_all.return_value = expected_restricciones

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == expected_restricciones
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_all_with_pagination(self):
        """Prueba get_all con parámetros de paginación"""
        # Arrange
        expected_restricciones = []
        self.mock_repo.get_all.return_value = expected_restricciones

        # Act
        result = self.use_cases.get_all(skip=10, limit=20)

        # Assert
        assert result == expected_restricciones
        self.mock_repo.get_all.assert_called_once_with(skip=10, limit=20)

    def test_get_by_id_returns_restriccion_when_exists(self):
        """Prueba que get_by_id retorna la restricción cuando existe"""
        # Arrange
        restriccion_id = 1
        expected_restriccion = Restriccion(
            id=restriccion_id,
            docente_id=1,
            tipo="horario",
            valor="08:00-12:00",
            prioridad=5,
            restriccion_blanda="Flexible",
            restriccion_dura=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.mock_repo.get_by_id.return_value = expected_restriccion

        # Act
        result = self.use_cases.get_by_id(restriccion_id)

        # Assert
        assert result == expected_restriccion
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)

    def test_get_by_id_raises_exception_when_not_exists(self):
        """Prueba que get_by_id lanza excepción cuando la restricción no existe"""
        # Arrange
        restriccion_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_id(restriccion_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Restricción no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)

    def test_create_restriccion_success(self):
        """Prueba creación exitosa de restricción"""
        # Arrange
        restriccion_data = RestriccionCreate(
            docente_id=1,
            tipo="horario",
            valor="08:00-12:00",
            prioridad=5,
            restriccion_blanda="Flexible",
            restriccion_dura=None
        )
        expected_restriccion = Restriccion(
            id=1,
            docente_id=1,
            tipo="horario",
            valor="08:00-12:00",
            prioridad=5,
            restriccion_blanda="Flexible",
            restriccion_dura=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.mock_repo.create.return_value = expected_restriccion

        # Act
        result = self.use_cases.create(restriccion_data)

        # Assert
        assert result == expected_restriccion
        self.mock_repo.create.assert_called_once_with(restriccion_data)

    def test_update_restriccion_success(self):
        """Prueba actualización exitosa de restricción"""
        # Arrange
        restriccion_id = 1
        update_data = {"prioridad": 8, "valor": "14:00-18:00"}
        existing_restriccion = Restriccion(
            id=restriccion_id,
            docente_id=1,
            tipo="horario",
            valor="08:00-12:00",
            prioridad=5,
            restriccion_blanda="Flexible",
            restriccion_dura=None
        )
        updated_restriccion = Restriccion(
            id=restriccion_id,
            docente_id=1,
            tipo="horario",
            valor="14:00-18:00",
            prioridad=8,
            restriccion_blanda="Flexible",
            restriccion_dura=None
        )
        
        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.update.return_value = updated_restriccion

        # Act
        result = self.use_cases.update(restriccion_id, **update_data)

        # Assert
        assert result == updated_restriccion
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)
        self.mock_repo.update.assert_called_once_with(restriccion_id, update_data)

    def test_update_restriccion_not_found(self):
        """Prueba actualización de restricción que no existe"""
        # Arrange
        restriccion_id = 999
        update_data = {"prioridad": 8}
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.update(restriccion_id, **update_data)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Restricción no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)
        self.mock_repo.update.assert_not_called()

    def test_update_restriccion_repository_fails(self):
        """Prueba cuando el repositorio falla en la actualización"""
        # Arrange
        restriccion_id = 1
        update_data = {"prioridad": 8}
        existing_restriccion = Restriccion(
            id=restriccion_id,
            docente_id=1,
            tipo="horario",
            valor="08:00-12:00",
            prioridad=5,
            restriccion_blanda="Flexible",
            restriccion_dura=None
        )
        
        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.update.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.update(restriccion_id, **update_data)
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error al actualizar la restricción" in str(exc_info.value.detail)

    def test_delete_restriccion_success(self):
        """Prueba eliminación exitosa de restricción"""
        # Arrange
        restriccion_id = 1
        existing_restriccion = Restriccion(
            id=restriccion_id,
            docente_id=1,
            tipo="horario",
            valor="08:00-12:00",
            prioridad=5,
            restriccion_blanda="Flexible",
            restriccion_dura=None
        )
        
        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.delete.return_value = True

        # Act
        result = self.use_cases.delete(restriccion_id)

        # Assert
        assert result is True
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)
        self.mock_repo.delete.assert_called_once_with(restriccion_id)

    def test_delete_restriccion_not_found(self):
        """Prueba eliminación de restricción que no existe"""
        # Arrange
        restriccion_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.delete(restriccion_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Restricción no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)
        self.mock_repo.delete.assert_not_called()

    def test_delete_restriccion_repository_fails(self):
        """Prueba cuando el repositorio falla en la eliminación"""
        # Arrange
        restriccion_id = 1
        existing_restriccion = Restriccion(
            id=restriccion_id,
            docente_id=1,
            tipo="horario",
            valor="08:00-12:00",
            prioridad=5,
            restriccion_blanda="Flexible",
            restriccion_dura=None
        )
        
        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.delete.return_value = False

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.delete(restriccion_id)
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error al eliminar la restricción" in str(exc_info.value.detail)