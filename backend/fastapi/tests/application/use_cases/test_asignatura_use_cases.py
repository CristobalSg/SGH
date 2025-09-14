import pytest
from unittest.mock import Mock, create_autospec
from fastapi import HTTPException, status
from typing import List

# Importaciones del sistema bajo prueba
from application.use_cases.asignatura_use_cases import AsignaturaUseCases
from infrastructure.repositories.asignatura_repository import AsignaturaRepository
from domain.entities import Asignatura, AsignaturaCreate


class TestAsignaturaUseCases:
    """Pruebas unitarias para el caso de uso AsignaturaUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(AsignaturaRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_cases = AsignaturaUseCases(self.mock_repo)

    def test_get_all_returns_all_asignaturas(self):
        """Prueba que get_all retorna todas las asignaturas del repositorio"""
        # Arrange
        expected_asignaturas = [
            Asignatura(
                id=1,
                codigo="PROG1",
                nombre="Programación I",
                horas_semanales=6,
                creditos=4
            ),
            Asignatura(
                id=2,
                codigo="MATE1",
                nombre="Matemáticas I",
                horas_semanales=4,
                creditos=3
            )
        ]
        self.mock_repo.get_all.return_value = expected_asignaturas

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == expected_asignaturas
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_all_with_pagination(self):
        """Prueba get_all con parámetros de paginación"""
        # Arrange
        expected_asignaturas = []
        self.mock_repo.get_all.return_value = expected_asignaturas

        # Act
        result = self.use_cases.get_all(skip=10, limit=20)

        # Assert
        assert result == expected_asignaturas
        self.mock_repo.get_all.assert_called_once_with(skip=10, limit=20)

    def test_get_by_id_returns_asignatura_when_exists(self):
        """Prueba que get_by_id retorna la asignatura cuando existe"""
        # Arrange
        asignatura_id = 1
        expected_asignatura = Asignatura(
            id=asignatura_id,
            codigo="PROG1",
            nombre="Programación I",
            horas_semanales=6,
            creditos=4
        )
        self.mock_repo.get_by_id.return_value = expected_asignatura

        # Act
        result = self.use_cases.get_by_id(asignatura_id)

        # Assert
        assert result == expected_asignatura
        self.mock_repo.get_by_id.assert_called_once_with(asignatura_id)

    def test_get_by_id_raises_exception_when_not_exists(self):
        """Prueba que get_by_id lanza excepción cuando la asignatura no existe"""
        # Arrange
        asignatura_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_id(asignatura_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Asignatura no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(asignatura_id)

    def test_get_by_codigo_returns_asignatura_when_exists(self):
        """Prueba que get_by_codigo retorna la asignatura cuando existe"""
        # Arrange
        codigo = "PROG1"
        expected_asignatura = Asignatura(
            id=1,
            codigo=codigo,
            nombre="Programación I",
            horas_semanales=6,
            creditos=4
        )
        self.mock_repo.get_by_codigo.return_value = expected_asignatura

        # Act
        result = self.use_cases.get_by_codigo(codigo)

        # Assert
        assert result == expected_asignatura
        self.mock_repo.get_by_codigo.assert_called_once_with(codigo)

    def test_get_by_codigo_raises_exception_when_not_exists(self):
        """Prueba que get_by_codigo lanza excepción cuando la asignatura no existe"""
        # Arrange
        codigo = "INVALID"
        self.mock_repo.get_by_codigo.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_codigo(codigo)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Asignatura no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_codigo.assert_called_once_with(codigo)

    def test_create_asignatura_success(self):
        """Prueba creación exitosa de asignatura"""
        # Arrange
        asignatura_data = AsignaturaCreate(
            codigo="PROG1",
            nombre="Programación I",
            horas_semanales=6,
            creditos=4
        )
        expected_asignatura = Asignatura(
            id=1,
            codigo="PROG1",
            nombre="Programación I",
            horas_semanales=6,
            creditos=4
        )
        self.mock_repo.get_by_codigo.return_value = None  # Código no existe
        self.mock_repo.create.return_value = expected_asignatura

        # Act
        result = self.use_cases.create(asignatura_data)

        # Assert
        assert result == expected_asignatura
        self.mock_repo.get_by_codigo.assert_called_once_with("PROG1")
        self.mock_repo.create.assert_called_once_with(asignatura_data)

    def test_create_asignatura_codigo_already_exists(self):
        """Prueba creación de asignatura con código que ya existe"""
        # Arrange
        asignatura_data = AsignaturaCreate(
            codigo="PROG1",
            nombre="Programación I",
            horas_semanales=6,
            creditos=4
        )
        existing_asignatura = Asignatura(
            id=1,
            codigo="PROG1",
            nombre="Programación Existente",
            horas_semanales=4,
            creditos=3
        )
        self.mock_repo.get_by_codigo.return_value = existing_asignatura

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.create(asignatura_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "El código de asignatura ya existe" in str(exc_info.value.detail)
        self.mock_repo.get_by_codigo.assert_called_once_with("PROG1")
        self.mock_repo.create.assert_not_called()

    def test_update_asignatura_success(self):
        """Prueba actualización exitosa de asignatura"""
        # Arrange
        asignatura_id = 1
        update_data = {"nombre": "Programación Avanzada", "creditos": 5}
        existing_asignatura = Asignatura(
            id=asignatura_id,
            codigo="PROG1",
            nombre="Programación I",
            horas_semanales=6,
            creditos=4
        )
        updated_asignatura = Asignatura(
            id=asignatura_id,
            codigo="PROG1",
            nombre="Programación Avanzada",
            horas_semanales=6,
            creditos=5
        )
        
        self.mock_repo.get_by_id.return_value = existing_asignatura
        self.mock_repo.update.return_value = updated_asignatura

        # Act
        result = self.use_cases.update(asignatura_id, **update_data)

        # Assert
        assert result == updated_asignatura
        self.mock_repo.get_by_id.assert_called_once_with(asignatura_id)
        self.mock_repo.update.assert_called_once_with(asignatura_id, update_data)

    def test_update_asignatura_not_found(self):
        """Prueba actualización de asignatura que no existe"""
        # Arrange
        asignatura_id = 999
        update_data = {"nombre": "Nueva Asignatura"}
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.update(asignatura_id, **update_data)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Asignatura no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(asignatura_id)
        self.mock_repo.update.assert_not_called()

    def test_delete_asignatura_success(self):
        """Prueba eliminación exitosa de asignatura"""
        # Arrange
        asignatura_id = 1
        existing_asignatura = Asignatura(
            id=asignatura_id,
            codigo="PROG1",
            nombre="Programación I",
            horas_semanales=6,
            creditos=4
        )
        
        self.mock_repo.get_by_id.return_value = existing_asignatura
        self.mock_repo.has_secciones.return_value = False  # No tiene secciones
        self.mock_repo.delete.return_value = True

        # Act
        result = self.use_cases.delete(asignatura_id)

        # Assert
        assert result is True
        self.mock_repo.get_by_id.assert_called_once_with(asignatura_id)
        self.mock_repo.delete.assert_called_once_with(asignatura_id)

    def test_delete_asignatura_not_found(self):
        """Prueba eliminación de asignatura que no existe"""
        # Arrange
        asignatura_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.delete(asignatura_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Asignatura no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(asignatura_id)
        self.mock_repo.delete.assert_not_called()