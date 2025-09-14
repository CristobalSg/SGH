import pytest
from unittest.mock import Mock, create_autospec
from fastapi import HTTPException, status
from typing import List

# Importaciones del sistema bajo prueba
from application.use_cases.clase_uses_cases import ClaseUseCases
from infrastructure.repositories.clase_repository import ClaseRepository
from domain.entities import Clase, ClaseCreate


class TestClaseUseCases:
    """Pruebas unitarias para el caso de uso ClaseUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(ClaseRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_cases = ClaseUseCases(self.mock_repo)

    def test_get_all_returns_all_clases(self):
        """Prueba que get_all retorna todas las clases del repositorio"""
        # Arrange
        expected_clases = [
            Clase(
                id=1,
                seccion_id=1,
                sala_id=1,
                bloque_id=1,
                fecha="2024-09-14",
                estado="programada"
            ),
            Clase(
                id=2,
                seccion_id=1,
                sala_id=2,
                bloque_id=2,
                fecha="2024-09-15",
                estado="programada"
            )
        ]
        self.mock_repo.get_all.return_value = expected_clases

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == expected_clases
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_by_id_returns_clase_when_exists(self):
        """Prueba que get_by_id retorna la clase cuando existe"""
        # Arrange
        clase_id = 1
        expected_clase = Clase(
            id=clase_id,
            seccion_id=1,
            sala_id=1,
            bloque_id=1,
            fecha="2024-09-14",
            estado="programada"
        )
        self.mock_repo.get_by_id.return_value = expected_clase

        # Act
        result = self.use_cases.get_by_id(clase_id)

        # Assert
        assert result == expected_clase
        self.mock_repo.get_by_id.assert_called_once_with(clase_id)

    def test_get_by_id_raises_exception_when_not_exists(self):
        """Prueba que get_by_id lanza excepción cuando la clase no existe"""
        # Arrange
        clase_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_id(clase_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Clase no encontrada" in str(exc_info.value.detail)

    def test_create_clase_success(self):
        """Prueba creación exitosa de clase"""
        # Arrange
        clase_data = ClaseCreate(
            seccion_id=1,
            sala_id=1,
            bloque_id=1,
            fecha="2024-09-14",
            estado="programada"
        )
        expected_clase = Clase(
            id=1,
            seccion_id=1,
            sala_id=1,
            bloque_id=1,
            fecha="2024-09-14",
            estado="programada"
        )
        self.mock_repo.get_by_sala_bloque_fecha.return_value = None  # No hay conflicto
        self.mock_repo.create.return_value = expected_clase

        # Act
        result = self.use_cases.create(clase_data)

        # Assert
        assert result == expected_clase
        self.mock_repo.get_by_sala_bloque_fecha.assert_called_once_with(1, 1, "2024-09-14")
        self.mock_repo.create.assert_called_once_with(clase_data)

    def test_create_clase_conflict_exists(self):
        """Prueba creación de clase con conflicto de sala"""
        # Arrange
        clase_data = ClaseCreate(
            seccion_id=1,
            sala_id=1,
            bloque_id=1,
            fecha="2024-09-14",
            estado="programada"
        )
        conflicting_clase = Clase(
            id=1,
            seccion_id=2,
            sala_id=1,
            bloque_id=1,
            fecha="2024-09-14",
            estado="programada"
        )
        self.mock_repo.get_by_sala_bloque_fecha.return_value = conflicting_clase

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.create(clase_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe una clase programada" in str(exc_info.value.detail)

    def test_update_clase_success(self):
        """Prueba actualización exitosa de clase"""
        # Arrange
        clase_id = 1
        update_data = {"sala_id": 2, "estado": "realizada"}
        existing_clase = Clase(
            id=clase_id,
            seccion_id=1,
            sala_id=1,
            bloque_id=1,
            fecha="2024-09-14",
            estado="programada"
        )
        updated_clase = Clase(
            id=clase_id,
            seccion_id=1,
            sala_id=2,
            bloque_id=1,
            fecha="2024-09-14",
            estado="realizada"
        )
        
        self.mock_repo.get_by_id.return_value = existing_clase
        self.mock_repo.update.return_value = updated_clase

        # Act
        result = self.use_cases.update(clase_id, **update_data)

        # Assert
        assert result == updated_clase
        self.mock_repo.get_by_id.assert_called_once_with(clase_id)
        self.mock_repo.update.assert_called_once_with(clase_id, update_data)

    def test_delete_clase_success(self):
        """Prueba eliminación exitosa de clase"""
        # Arrange
        clase_id = 1
        existing_clase = Clase(
            id=clase_id,
            seccion_id=1,
            sala_id=1,
            bloque_id=1,
            fecha="2024-09-14",
            estado="programada"
        )
        
        self.mock_repo.get_by_id.return_value = existing_clase
        self.mock_repo.delete.return_value = True

        # Act
        result = self.use_cases.delete(clase_id)

        # Assert
        assert result is True
        self.mock_repo.get_by_id.assert_called_once_with(clase_id)
        self.mock_repo.delete.assert_called_once_with(clase_id)