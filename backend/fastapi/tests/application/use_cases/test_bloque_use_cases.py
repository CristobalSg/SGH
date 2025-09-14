import pytest
from unittest.mock import Mock, create_autospec
from fastapi import HTTPException, status
from typing import List

# Importaciones del sistema bajo prueba
from application.use_cases.bloque_use_cases import BloqueUseCases
from infrastructure.repositories.bloque_repository import BloqueRepository
from domain.entities import Bloque, BloqueCreate


class TestBloqueUseCases:
    """Pruebas unitarias para el caso de uso BloqueUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(BloqueRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_cases = BloqueUseCases(self.mock_repo)

    def test_get_all_returns_all_bloques(self):
        """Prueba que get_all retorna todos los bloques del repositorio"""
        # Arrange
        expected_bloques = [
            Bloque(
                id=1,
                numero=1,
                hora_inicio="08:00",
                hora_fin="09:30",
                dia_semana=1
            ),
            Bloque(
                id=2,
                numero=2,
                hora_inicio="09:45",
                hora_fin="11:15",
                dia_semana=1
            )
        ]
        self.mock_repo.get_all.return_value = expected_bloques

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == expected_bloques
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_by_id_returns_bloque_when_exists(self):
        """Prueba que get_by_id retorna el bloque cuando existe"""
        # Arrange
        bloque_id = 1
        expected_bloque = Bloque(
            id=bloque_id,
            numero=1,
            hora_inicio="08:00",
            hora_fin="09:30",
            dia_semana=1
        )
        self.mock_repo.get_by_id.return_value = expected_bloque

        # Act
        result = self.use_cases.get_by_id(bloque_id)

        # Assert
        assert result == expected_bloque
        self.mock_repo.get_by_id.assert_called_once_with(bloque_id)

    def test_get_by_id_raises_exception_when_not_exists(self):
        """Prueba que get_by_id lanza excepción cuando el bloque no existe"""
        # Arrange
        bloque_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_id(bloque_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Bloque no encontrado" in str(exc_info.value.detail)

    def test_create_bloque_success(self):
        """Prueba creación exitosa de bloque"""
        # Arrange
        bloque_data = BloqueCreate(
            numero=1,
            hora_inicio="08:00",
            hora_fin="09:30",
            dia_semana=1
        )
        expected_bloque = Bloque(
            id=1,
            numero=1,
            hora_inicio="08:00",
            hora_fin="09:30",
            dia_semana=1
        )
        self.mock_repo.get_by_numero_and_dia.return_value = None  # No existe
        self.mock_repo.create.return_value = expected_bloque

        # Act
        result = self.use_cases.create(bloque_data)

        # Assert
        assert result == expected_bloque
        self.mock_repo.get_by_numero_and_dia.assert_called_once_with(1, 1)
        self.mock_repo.create.assert_called_once_with(bloque_data)

    def test_create_bloque_already_exists(self):
        """Prueba creación de bloque que ya existe"""
        # Arrange
        bloque_data = BloqueCreate(
            numero=1,
            hora_inicio="08:00",
            hora_fin="09:30",
            dia_semana=1
        )
        existing_bloque = Bloque(
            id=1,
            numero=1,
            hora_inicio="08:00",
            hora_fin="09:30",
            dia_semana=1
        )
        self.mock_repo.get_by_numero_and_dia.return_value = existing_bloque

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.create(bloque_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe un bloque" in str(exc_info.value.detail)

    def test_update_bloque_success(self):
        """Prueba actualización exitosa de bloque"""
        # Arrange
        bloque_id = 1
        update_data = {"hora_inicio": "08:30", "hora_fin": "10:00"}
        existing_bloque = Bloque(
            id=bloque_id,
            numero=1,
            hora_inicio="08:00",
            hora_fin="09:30",
            dia_semana=1
        )
        updated_bloque = Bloque(
            id=bloque_id,
            numero=1,
            hora_inicio="08:30",
            hora_fin="10:00",
            dia_semana=1
        )
        
        self.mock_repo.get_by_id.return_value = existing_bloque
        self.mock_repo.update.return_value = updated_bloque

        # Act
        result = self.use_cases.update(bloque_id, **update_data)

        # Assert
        assert result == updated_bloque
        self.mock_repo.get_by_id.assert_called_once_with(bloque_id)
        self.mock_repo.update.assert_called_once_with(bloque_id, update_data)

    def test_delete_bloque_success(self):
        """Prueba eliminación exitosa de bloque"""
        # Arrange
        bloque_id = 1
        existing_bloque = Bloque(
            id=bloque_id,
            numero=1,
            hora_inicio="08:00",
            hora_fin="09:30",
            dia_semana=1
        )
        
        self.mock_repo.get_by_id.return_value = existing_bloque
        self.mock_repo.delete.return_value = True

        # Act
        result = self.use_cases.delete(bloque_id)

        # Assert
        assert result is True
        self.mock_repo.get_by_id.assert_called_once_with(bloque_id)
        self.mock_repo.delete.assert_called_once_with(bloque_id)