import pytest
from unittest.mock import Mock, create_autospec, call
from datetime import time
from typing import List, Optional

from fastapi import HTTPException, status

# Importaciones del sistema bajo prueba
from application.use_cases.restriccion_horario_use_cases import RestriccionHorarioUseCases
from infrastructure.repositories.restriccion_horario_repository import RestriccionHorarioRepository
from domain.entities import RestriccionHorario, RestriccionHorarioCreate


class TestRestriccionHorarioUseCases:
    """Pruebas unitarias para el caso de uso RestriccionHorarioUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        # Crear un mock del repositorio
        self.mock_repo = create_autospec(RestriccionHorarioRepository)
        # Crear la instancia del caso de uso con el mock
        self.use_cases = RestriccionHorarioUseCases(self.mock_repo)

    def test_get_all_returns_all_restricciones(self):
        """Prueba que get_all retorna todas las restricciones de horario del repositorio"""
        # Arrange
        expected_restricciones = [
            RestriccionHorario(
                id=1,
                docente_id=1,
                dia_semana=1,
                hora_inicio=time(8, 0),
                hora_fin=time(10, 0),
                disponible=True,
                descripcion="Disponible mañanas"
            ),
            RestriccionHorario(
                id=2,
                docente_id=1,
                dia_semana=2,
                hora_inicio=time(14, 0),
                hora_fin=time(16, 0),
                disponible=False,
                descripcion="No disponible tardes"
            )
        ]
        self.mock_repo.get_all.return_value = expected_restricciones

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == expected_restricciones
        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=100)

    def test_get_all_returns_empty_list_when_no_restricciones(self):
        """Prueba que get_all retorna lista vacía cuando no hay restricciones"""
        # Arrange
        self.mock_repo.get_all.return_value = []

        # Act
        result = self.use_cases.get_all()

        # Assert
        assert result == []
        self.mock_repo.get_all.assert_called_once()

    def test_get_by_id_returns_restriccion_when_exists(self):
        """Prueba que get_by_id retorna la restricción cuando existe"""
        # Arrange
        restriccion_id = 1
        expected_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=1,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=True,
            descripcion="Test restricción"
        )
        self.mock_repo.get_by_id.return_value = expected_restriccion

        # Act
        result = self.use_cases.get_by_id(restriccion_id)

        # Assert
        assert result == expected_restriccion
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)

    def test_get_by_id_returns_none_when_not_exists(self):
        """Prueba que get_by_id lanza HTTPException cuando la restricción no existe"""
        # Arrange
        restriccion_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.get_by_id(restriccion_id)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Restricción de horario no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)

    def test_create_creates_and_returns_new_restriccion(self):
        """Prueba que create crea y retorna una nueva restricción"""
        # Arrange
        docente_id = 1
        dia_semana = 2
        hora_inicio = "08:00"
        hora_fin = "10:00"
        disponible = True
        descripcion = "Nueva restricción"

        expected_restriccion = RestriccionHorario(
            id=1,
            docente_id=docente_id,
            dia_semana=dia_semana,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=disponible,
            descripcion=descripcion
        )
        self.mock_repo.get_by_docente_y_horario.return_value = []  # No hay conflictos
        self.mock_repo.create.return_value = expected_restriccion

        # Act
        restriccion_data = RestriccionHorarioCreate(
            docente_id=docente_id,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            disponible=disponible,
            descripcion=descripcion
        )
        result = self.use_cases.create(restriccion_data)

        # Assert
        assert result == expected_restriccion
        self.mock_repo.create.assert_called_once()
        
        # Verificar que se llamó con una RestriccionHorarioCreate con los valores correctos
        call_args = self.mock_repo.create.call_args[0][0]
        assert call_args.docente_id == docente_id
        assert call_args.dia_semana == dia_semana
        assert call_args.hora_inicio == time(8, 0)  # Convertido por Pydantic
        assert call_args.hora_fin == time(10, 0)    # Convertido por Pydantic
        assert call_args.disponible == disponible
        assert call_args.descripcion == descripcion

    def test_create_with_default_descripcion(self):
        """Prueba que create funciona con descripción por defecto (None)"""
        # Arrange
        docente_id = 1
        dia_semana = 2
        hora_inicio = "08:00"
        hora_fin = "10:00"
        disponible = True

        expected_restriccion = RestriccionHorario(
            id=1,
            docente_id=docente_id,
            dia_semana=dia_semana,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=disponible,
            descripcion=None
        )
        self.mock_repo.get_by_docente_y_horario.return_value = []  # No hay conflictos
        self.mock_repo.create.return_value = expected_restriccion

        # Act
        restriccion_data = RestriccionHorarioCreate(
            docente_id=docente_id,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            disponible=disponible
        )
        result = self.use_cases.create(restriccion_data)

        # Assert
        assert result == expected_restriccion
        self.mock_repo.create.assert_called_once()

        call_args = self.mock_repo.create.call_args[0][0]
        assert call_args.descripcion is None

    def test_update_updates_existing_restriccion(self):
        """Prueba que update actualiza una restricción existente"""
        # Arrange
        restriccion_id = 1
        existing_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=1,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=True,
            descripcion="Original"
        )
        
        updated_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=2,
            hora_inicio=time(9, 0),
            hora_fin=time(11, 0),
            disponible=False,
            descripcion="Actualizada"
        )

        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.update.return_value = updated_restriccion

        # Act
        result = self.use_cases.update(restriccion_id, 
            id=restriccion_id,
            dia_semana=2,
            hora_inicio="09:00",
            hora_fin="11:00",
            disponible=False,
            descripcion="Actualizada"
        )

        # Assert
        assert result == updated_restriccion
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)
        # Verificar que se llamó update con el ID y los datos de actualización
        self.mock_repo.update.assert_called_once_with(restriccion_id, {
            'id': restriccion_id,
            'dia_semana': 2,
            'hora_inicio': '09:00',
            'hora_fin': '11:00',
            'disponible': False,
            'descripcion': 'Actualizada'
        })

    def test_update_partial_update(self):
        """Prueba que update funciona con actualización parcial"""
        # Arrange
        restriccion_id = 1
        existing_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=1,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=True,
            descripcion="Original"
        )
        
        updated_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=2,  # Solo este campo se actualiza
            hora_inicio=time(8, 0),  # Los demás permanecen igual
            hora_fin=time(10, 0),
            disponible=True,
            descripcion="Original"
        )

        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.update.return_value = updated_restriccion

        # Act - Solo actualizamos dia_semana
        result = self.use_cases.update(restriccion_id, 
            id=restriccion_id,
            dia_semana=2
        )

        # Assert
        assert result == updated_restriccion
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)
        # Verificar que se llamó update con el ID y los datos de actualización
        self.mock_repo.update.assert_called_once_with(restriccion_id, {
            'id': restriccion_id,
            'dia_semana': 2
        })

    def test_update_returns_none_when_restriccion_not_exists(self):
        """Prueba que update lanza HTTPException cuando la restricción no existe"""
        # Arrange
        restriccion_id = 999
        self.mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.update(restriccion_id, 
                id=restriccion_id,
                dia_semana=2
            )
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Restricción de horario no encontrada" in str(exc_info.value.detail)
        self.mock_repo.get_by_id.assert_called_once_with(restriccion_id)
        self.mock_repo.update.assert_not_called()

    def test_update_disponible_false_explicitly(self):
        """Prueba que update maneja correctamente disponible=False"""
        # Arrange
        restriccion_id = 1
        existing_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=1,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=True,
            descripcion="Original"
        )

        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.update.return_value = existing_restriccion

        # Act - Establecer disponible explícitamente a False
        result = self.use_cases.update(restriccion_id, 
            id=restriccion_id,
            disponible=False
        )

        # Assert
        # Verificar que se llamó update con los datos correctos
        self.mock_repo.update.assert_called_once_with(restriccion_id, {
            'id': restriccion_id,
            'disponible': False
        })

    def test_delete_returns_true_when_successful(self):
        """Prueba que delete retorna True cuando la eliminación es exitosa"""
        # Arrange
        restriccion_id = 1
        self.mock_repo.delete.return_value = True

        # Act
        result = self.use_cases.delete(restriccion_id)

        # Assert
        assert result == True
        self.mock_repo.delete.assert_called_once_with(restriccion_id)

    def test_delete_returns_false_when_fails(self):
        """Prueba que delete lanza HTTPException cuando la eliminación falla"""
        # Arrange
        restriccion_id = 999
        existing_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=1,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=True,
            descripcion="Restricción de prueba"
        )
        self.mock_repo.get_by_id.return_value = existing_restriccion
        self.mock_repo.delete.return_value = False

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.use_cases.delete(restriccion_id)
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error al eliminar la restricción de horario" in str(exc_info.value.detail)
        self.mock_repo.delete.assert_called_once_with(restriccion_id)


class TestRestriccionHorarioUseCasesIntegration:
    """Pruebas de integración más complejas para RestriccionHorarioUseCases"""

    def setup_method(self):
        """Configuración que se ejecuta antes de cada prueba"""
        self.mock_repo = create_autospec(RestriccionHorarioRepository)
        self.use_cases = RestriccionHorarioUseCases(self.mock_repo)

    def test_create_update_delete_workflow(self):
        """Prueba el flujo completo de crear, actualizar y eliminar una restricción"""
        # Arrange
        docente_id = 1
        dia_semana = 1
        hora_inicio = "08:00"
        hora_fin = "10:00"
        disponible = True
        descripcion = "Restricción de prueba"

        # Restricción creada
        created_restriccion = RestriccionHorario(
            id=1,
            docente_id=docente_id,
            dia_semana=dia_semana,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=disponible,
            descripcion=descripcion
        )

        # Restricción actualizada
        updated_restriccion = RestriccionHorario(
            id=1,
            docente_id=docente_id,
            dia_semana=2,  # Cambiado
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=False,  # Cambiado
            descripcion="Restricción actualizada"  # Cambiado
        )

        # Setup mocks
        self.mock_repo.get_by_docente_y_horario.return_value = []  # No hay conflictos para crear
        self.mock_repo.create.return_value = created_restriccion
        self.mock_repo.get_by_id.return_value = created_restriccion
        self.mock_repo.update.return_value = updated_restriccion
        self.mock_repo.delete.return_value = True

        # Act & Assert - Create
        result_create = self.use_cases.create(
            RestriccionHorarioCreate(
                docente_id=docente_id,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                disponible=disponible,
                descripcion=descripcion
            )
        )
        assert result_create == created_restriccion

        # Act & Assert - Update
        result_update = self.use_cases.update(1, 
            id=1,
            dia_semana=2,
            disponible=False,
            descripcion="Restricción actualizada"
        )
        assert result_update == updated_restriccion

        # Act & Assert - Delete
        result_delete = self.use_cases.delete(1)
        assert result_delete == True

        # Verificar que todos los métodos del repositorio fueron llamados
        self.mock_repo.create.assert_called_once()
        # get_by_id se llama 2 veces: una en update y otra en delete
        assert self.mock_repo.get_by_id.call_count == 2
        self.mock_repo.update.assert_called_once()
        self.mock_repo.delete.assert_called_once_with(1)

    def test_multiple_updates_on_same_restriccion(self):
        """Prueba múltiples actualizaciones sobre la misma restricción"""
        # Arrange
        restriccion_id = 1
        base_restriccion = RestriccionHorario(
            id=restriccion_id,
            docente_id=1,
            dia_semana=1,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            disponible=True,
            descripcion="Original"
        )

        self.mock_repo.get_by_id.return_value = base_restriccion
        self.mock_repo.update.return_value = base_restriccion

        # Act - Primera actualización
        self.use_cases.update(restriccion_id, id=restriccion_id, dia_semana=2)
        
        # Act - Segunda actualización
        self.use_cases.update(restriccion_id, id=restriccion_id, disponible=False)
        
        # Act - Tercera actualización
        self.use_cases.update(restriccion_id, id=restriccion_id, descripcion="Final")

        # Assert
        assert self.mock_repo.get_by_id.call_count == 3
        assert self.mock_repo.update.call_count == 3
        
        # Verificar las llamadas individuales de update
        expected_calls = [
            call(restriccion_id, {'id': restriccion_id, 'dia_semana': 2}),
            call(restriccion_id, {'id': restriccion_id, 'disponible': False}),
            call(restriccion_id, {'id': restriccion_id, 'descripcion': 'Final'})
        ]
        self.mock_repo.update.assert_has_calls(expected_calls)