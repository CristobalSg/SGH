import pytest
from fastapi import status
from datetime import time


class TestRestriccionHorarioIntegration:
    """Pruebas de integración para la API de restricciones de horario (/restricciones-horario)"""

    @pytest.fixture(autouse=True)
    def setup_docente(self, db_session, sample_docente_data):
        """Setup que crea un docente antes de cada prueba"""
        from domain.models import Docente
        # Crear docente en la base de datos para las pruebas
        docente = Docente(**sample_docente_data)
        db_session.add(docente)
        db_session.commit()
        db_session.refresh(docente)
        self.docente_id = docente.id

    def test_create_restriccion_horario_success(self, client, sample_restriccion_horario_data):
        """Prueba POST /restricciones-horario para crear una restricción de horario exitosamente"""
        # Usar el docente_id creado en setup
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        
        response = client.post("/restricciones-horario/", json=sample_restriccion_horario_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["docente_id"] == self.docente_id
        assert data["dia_semana"] == sample_restriccion_horario_data["dia_semana"]
        assert data["hora_inicio"] == sample_restriccion_horario_data["hora_inicio"]
        assert data["hora_fin"] == sample_restriccion_horario_data["hora_fin"]
        assert data["disponible"] == sample_restriccion_horario_data["disponible"]
        assert "id" in data

    def test_create_restriccion_horario_invalid_data(self, client):
        """Prueba POST /restricciones-horario con datos inválidos"""
        invalid_data = {
            "docente_id": -1,  # ID negativo
            "dia_semana": 8,  # Día inválido (0-6 válidos)
            "hora_inicio": "25:00",  # Hora inválida
            "hora_fin": "08:00",  # Hora fin menor que inicio
            "disponible": "not_boolean"  # No es booleano
        }
        
        response = client.post("/restricciones-horario/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_all_restricciones_horario_empty(self, client):
        """Prueba GET /restricciones-horario cuando no hay restricciones"""
        response = client.get("/restricciones-horario/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_all_restricciones_horario_with_pagination(self, client, sample_restriccion_horario_data):
        """Prueba GET /restricciones-horario con paginación"""
        # Crear varias restricciones
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        for i in range(5):
            restriccion_data = sample_restriccion_horario_data.copy()
            restriccion_data["dia_semana"] = i % 7
            client.post("/restricciones-horario/", json=restriccion_data)
        
        # Probar paginación
        response = client.get("/restricciones-horario/?skip=2&limit=2")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) <= 2

    def test_get_restriccion_horario_by_id_success(self, client, sample_restriccion_horario_data):
        """Prueba GET /restricciones-horario/{id} para obtener una restricción existente"""
        # Crear restricción primero
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        create_response = client.post("/restricciones-horario/", json=sample_restriccion_horario_data)
        created_restriccion = create_response.json()
        restriccion_id = created_restriccion["id"]
        
        # Obtener restricción por ID
        response = client.get(f"/restricciones-horario/{restriccion_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == restriccion_id
        assert data["docente_id"] == self.docente_id

    def test_get_restriccion_horario_by_id_not_found(self, client):
        """Prueba GET /restricciones-horario/{id} cuando la restricción no existe"""
        response = client.get("/restricciones-horario/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_restriccion_horario_success(self, client, sample_restriccion_horario_data):
        """Prueba PATCH /restricciones-horario/{id} para actualización parcial"""
        # Crear restricción primero
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        create_response = client.post("/restricciones-horario/", json=sample_restriccion_horario_data)
        restriccion_id = create_response.json()["id"]
        
        # Actualizar restricción parcialmente
        update_data = {
            "disponible": False,
            "descripcion": "Actualizada"
        }
        response = client.patch(f"/restricciones-horario/{restriccion_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == restriccion_id
        assert data["disponible"] is False
        assert data["descripcion"] == "Actualizada"

    def test_update_restriccion_horario_not_found(self, client):
        """Prueba PATCH /restricciones-horario/{id} cuando la restricción no existe"""
        update_data = {"disponible": False}
        response = client.patch("/restricciones-horario/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_restriccion_horario_empty_data(self, client, sample_restriccion_horario_data):
        """Prueba PATCH /restricciones-horario/{id} sin datos para actualizar"""
        # Crear restricción primero
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        create_response = client.post("/restricciones-horario/", json=sample_restriccion_horario_data)
        restriccion_id = create_response.json()["id"]
        
        # Intentar actualizar sin datos
        response = client.patch(f"/restricciones-horario/{restriccion_id}", json={})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "No se proporcionaron campos para actualizar" in response.json()["detail"]

    def test_delete_restriccion_horario_success(self, client, sample_restriccion_horario_data):
        """Prueba DELETE /restricciones-horario/{id} para eliminar una restricción"""
        # Crear restricción primero
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        create_response = client.post("/restricciones-horario/", json=sample_restriccion_horario_data)
        restriccion_id = create_response.json()["id"]
        
        # Eliminar restricción
        response = client.delete(f"/restricciones-horario/{restriccion_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que la restricción fue eliminada
        get_response = client.get(f"/restricciones-horario/{restriccion_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_restriccion_horario_not_found(self, client):
        """Prueba DELETE /restricciones-horario/{id} cuando la restricción no existe"""
        response = client.delete("/restricciones-horario/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_restricciones_by_docente(self, client, sample_restriccion_horario_data):
        """Prueba GET /restricciones-horario/docente/{docente_id}"""
        # Crear varias restricciones para el mismo docente
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        for dia in [1, 2, 3]:
            restriccion_data = sample_restriccion_horario_data.copy()
            restriccion_data["dia_semana"] = dia
            client.post("/restricciones-horario/", json=restriccion_data)
        
        response = client.get(f"/restricciones-horario/docente/{self.docente_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert all(restriccion["docente_id"] == self.docente_id for restriccion in data)

    def test_get_restricciones_by_dia(self, client, sample_restriccion_horario_data):
        """Prueba GET /restricciones-horario/dia/{dia_semana}"""
        # Crear restricciones para diferentes días
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        
        # Primera restricción para el lunes (día 1)
        restriccion_data_1 = sample_restriccion_horario_data.copy()
        restriccion_data_1["dia_semana"] = 1
        restriccion_data_1["hora_inicio"] = "08:00:00"
        restriccion_data_1["hora_fin"] = "10:00:00"
        client.post("/restricciones-horario/", json=restriccion_data_1)
        
        # Segunda restricción para el lunes (día 1) con horario diferente
        restriccion_data_2 = sample_restriccion_horario_data.copy()
        restriccion_data_2["dia_semana"] = 1
        restriccion_data_2["hora_inicio"] = "14:00:00"
        restriccion_data_2["hora_fin"] = "16:00:00"
        restriccion_data_2["descripcion"] = "Disponible en la tarde"
        client.post("/restricciones-horario/", json=restriccion_data_2)
        
        # Restricción para el martes (día 2)
        restriccion_data_3 = sample_restriccion_horario_data.copy()
        restriccion_data_3["dia_semana"] = 2
        client.post("/restricciones-horario/", json=restriccion_data_3)
        
        response = client.get("/restricciones-horario/dia/1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert all(restriccion["dia_semana"] == 1 for restriccion in data)

    def test_get_restricciones_by_dia_invalid(self, client):
        """Prueba GET /restricciones-horario/dia/{dia_semana} con día inválido"""
        response = client.get("/restricciones-horario/dia/8")  # Día inválido
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_disponibilidad_docente(self, client, sample_restriccion_horario_data):
        """Prueba GET /restricciones-horario/disponibilidad/{docente_id}"""
        # Crear restricciones con diferentes disponibilidades
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        
        # Restricción disponible
        disponible_data = sample_restriccion_horario_data.copy()
        disponible_data["disponible"] = True
        client.post("/restricciones-horario/", json=disponible_data)
        
        # Restricción no disponible
        no_disponible_data = sample_restriccion_horario_data.copy()
        no_disponible_data["dia_semana"] = 2
        no_disponible_data["disponible"] = False
        client.post("/restricciones-horario/", json=no_disponible_data)
        
        response = client.get(f"/restricciones-horario/disponibilidad/{self.docente_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1  # Solo la disponible
        assert data[0]["disponible"] is True

    def test_delete_restricciones_by_docente(self, client, sample_restriccion_horario_data):
        """Prueba DELETE /restricciones-horario/docente/{docente_id}"""
        # Crear varias restricciones para el docente
        sample_restriccion_horario_data["docente_id"] = self.docente_id
        for dia in [1, 2, 3]:
            restriccion_data = sample_restriccion_horario_data.copy()
            restriccion_data["dia_semana"] = dia
            client.post("/restricciones-horario/", json=restriccion_data)
        
        # Eliminar todas las restricciones del docente
        response = client.delete(f"/restricciones-horario/docente/{self.docente_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["eliminadas"] == 3
        assert "Se eliminaron 3 restricciones" in data["mensaje"]
        
        # Verificar que se eliminaron
        get_response = client.get(f"/restricciones-horario/docente/{self.docente_id}")
        assert get_response.json() == []