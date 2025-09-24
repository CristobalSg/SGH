import pytest
from fastapi import status
from domain.models import Docente, Restriccion


class TestRestriccionesIntegration:
    """Pruebas de integración para la API de restricciones (/restricciones)"""

    @pytest.fixture(autouse=True)
    def setup_docente(self, db_session, sample_docente_data):
        """Setup que crea un docente antes de cada prueba"""
        # Crear docente en la base de datos para las pruebas
        docente = Docente(**sample_docente_data)
        db_session.add(docente)
        db_session.commit()
        db_session.refresh(docente)
        self.docente_id = docente.id

    def test_get_all_restricciones_empty(self, client):
        """Prueba GET /restricciones cuando no hay restricciones"""
        response = client.get("/restricciones/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_restriccion_success(self, authenticated_client, sample_restriccion_data):
        """Prueba POST /restricciones para crear una restricción exitosamente"""
        # Usar el docente_id creado en setup
        sample_restriccion_data["docente_id"] = self.docente_id
        
        response = authenticated_client.post("/restricciones/", json=sample_restriccion_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["docente_id"] == self.docente_id
        assert data["tipo"] == sample_restriccion_data["tipo"]
        assert data["valor"] == sample_restriccion_data["valor"]
        assert data["prioridad"] == sample_restriccion_data["prioridad"]
        assert data["restriccion_blanda"] == sample_restriccion_data["restriccion_blanda"]
        assert data["restriccion_dura"] == sample_restriccion_data["restriccion_dura"]
        assert "id" in data

    def test_create_restriccion_invalid_data(self, authenticated_client):
        """Prueba POST /restricciones con datos inválidos"""
        invalid_data = {
            "docente_id": -1,  # ID negativo
            "tipo": "tipo_invalido",  # Tipo no válido
            "valor": "",  # Valor vacío
            "prioridad": 15  # Prioridad fuera de rango
        }
        
        response = authenticated_client.post("/restricciones/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_restriccion_missing_fields(self, authenticated_client):
        """Prueba POST /restricciones con campos requeridos faltantes"""
        incomplete_data = {
            "docente_id": self.docente_id,
            "tipo": "horario"
            # Faltan campos requeridos
        }
        
        response = authenticated_client.post("/restricciones/", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_restriccion_by_id_success(self, authenticated_client, sample_restriccion_data):
        """Prueba GET /restricciones/{id} para obtener una restricción existente"""
        # Crear restricción primero
        sample_restriccion_data["docente_id"] = self.docente_id
        create_response = authenticated_client.post("/restricciones/", json=sample_restriccion_data)
        created_restriccion = create_response.json()
        restriccion_id = created_restriccion["id"]
        
        # Obtener restricción por ID
        response = authenticated_client.get(f"/restricciones/{restriccion_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == restriccion_id
        assert data["docente_id"] == self.docente_id
        assert data["tipo"] == sample_restriccion_data["tipo"]

    def test_get_restriccion_by_id_not_found(self, client):
        """Prueba GET /restricciones/{id} cuando la restricción no existe"""
        response = client.get("/restricciones/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrada" in response.json()["detail"]

    def test_get_restriccion_by_id_invalid_id(self, client):
        """Prueba GET /restricciones/{id} con ID inválido"""
        response = client.get("/restricciones/0")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_all_restricciones_with_data(self, authenticated_client, sample_restriccion_data):
        """Prueba GET /restricciones cuando hay restricciones en la base de datos"""
        # Crear múltiples restricciones
        sample_restriccion_data["docente_id"] = self.docente_id
        
        restriccion1_data = sample_restriccion_data.copy()
        restriccion2_data = sample_restriccion_data.copy()
        restriccion2_data["tipo"] = "aula"
        restriccion2_data["valor"] = "Sala A"
        
        authenticated_client.post("/restricciones/", json=restriccion1_data)
        authenticated_client.post("/restricciones/", json=restriccion2_data)
        
        # Obtener todas las restricciones
        response = authenticated_client.get("/restricciones/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert all("id" in restriccion for restriccion in data)
        assert any(restriccion["tipo"] == "horario" for restriccion in data)
        assert any(restriccion["tipo"] == "aula" for restriccion in data)

    def test_update_restriccion_complete_success(self, authenticated_client, sample_restriccion_data, sample_restriccion_update_data):
        """Prueba PUT /restricciones/{id} para actualización completa"""
        # Crear restricción primero
        sample_restriccion_data["docente_id"] = self.docente_id
        create_response = authenticated_client.post("/restricciones/", json=sample_restriccion_data)
        restriccion_id = create_response.json()["id"]
        
        # Actualizar restricción completa
        response = authenticated_client.put(f"/restricciones/{restriccion_id}", json=sample_restriccion_update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == restriccion_id
        assert data["tipo"] == sample_restriccion_update_data["tipo"]
        assert data["valor"] == sample_restriccion_update_data["valor"]
        assert data["prioridad"] == sample_restriccion_update_data["prioridad"]

    def test_update_restriccion_complete_not_found(self, authenticated_client, sample_restriccion_update_data):
        """Prueba PUT /restricciones/{id} cuando la restricción no existe"""
        response = authenticated_client.put("/restricciones/999", json=sample_restriccion_update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrada" in response.json()["detail"]

    def test_update_restriccion_partial_success(self, authenticated_client, sample_restriccion_data, sample_restriccion_patch_data):
        """Prueba PATCH /restricciones/{id} para actualización parcial"""
        # Crear restricción primero
        sample_restriccion_data["docente_id"] = self.docente_id
        create_response = authenticated_client.post("/restricciones/", json=sample_restriccion_data)
        created_data = create_response.json()
        restriccion_id = created_data["id"]
        
        # Actualizar restricción parcialmente
        response = authenticated_client.patch(f"/restricciones/{restriccion_id}", json=sample_restriccion_patch_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == restriccion_id
        assert data["prioridad"] == sample_restriccion_patch_data["prioridad"]
        assert data["restriccion_blanda"] == sample_restriccion_patch_data["restriccion_blanda"]
        # Verificar que otros campos no cambiaron
        assert data["tipo"] == sample_restriccion_data["tipo"]
        assert data["valor"] == sample_restriccion_data["valor"]

    def test_update_restriccion_partial_empty_data(self, authenticated_client, sample_restriccion_data):
        """Prueba PATCH /restricciones/{id} sin datos para actualizar"""
        # Crear restricción primero
        sample_restriccion_data["docente_id"] = self.docente_id
        create_response = authenticated_client.post("/restricciones/", json=sample_restriccion_data)
        restriccion_id = create_response.json()["id"]
        
        # Intentar actualizar sin datos
        response = authenticated_client.patch(f"/restricciones/{restriccion_id}", json={})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "No se proporcionaron datos" in response.json()["detail"]

    def test_update_restriccion_partial_not_found(self, authenticated_client, sample_restriccion_patch_data):
        """Prueba PATCH /restricciones/{id} cuando la restricción no existe"""
        response = authenticated_client.patch("/restricciones/999", json=sample_restriccion_patch_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrada" in response.json()["detail"]

    def test_delete_restriccion_success(self, authenticated_client, sample_restriccion_data):
        """Prueba DELETE /restricciones/{id} para eliminar una restricción"""
        # Crear restricción primero
        sample_restriccion_data["docente_id"] = self.docente_id
        create_response = authenticated_client.post("/restricciones/", json=sample_restriccion_data)
        restriccion_id = create_response.json()["id"]
        
        # Eliminar restricción
        response = authenticated_client.delete(f"/restricciones/{restriccion_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b''
        
        # Verificar que la restricción fue eliminada
        get_response = authenticated_client.get(f"/restricciones/{restriccion_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_restriccion_not_found(self, authenticated_client):
        """Prueba DELETE /restricciones/{id} cuando la restricción no existe"""
        response = authenticated_client.delete("/restricciones/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrada" in response.json()["detail"]

    def test_delete_restriccion_invalid_id(self, authenticated_client):
        """Prueba DELETE /restricciones/{id} con ID inválido"""
        response = authenticated_client.delete("/restricciones/0")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestRestriccionesWorkflow:
    """Pruebas de flujo completo de la API de restricciones"""

    @pytest.fixture(autouse=True)
    def setup_docente(self, db_session, sample_docente_data):
        """Setup que crea un docente antes de cada prueba"""
        docente = Docente(**sample_docente_data)
        db_session.add(docente)
        db_session.commit()
        db_session.refresh(docente)
        self.docente_id = docente.id

    def test_full_crud_workflow(self, authenticated_client, sample_restriccion_data, sample_restriccion_update_data, sample_restriccion_patch_data):
        """Prueba el flujo completo CRUD: Create, Read, Update, Delete"""
        sample_restriccion_data["docente_id"] = self.docente_id
        
        # 1. CREATE - Crear restricción
        create_response = authenticated_client.post("/restricciones/", json=sample_restriccion_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_data = create_response.json()
        restriccion_id = created_data["id"]
        
        # 2. READ - Obtener restricción creada
        get_response = authenticated_client.get(f"/restricciones/{restriccion_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["id"] == restriccion_id
        
        # 3. UPDATE (completa) - Actualizar restricción
        update_response = authenticated_client.put(f"/restricciones/{restriccion_id}", json=sample_restriccion_update_data)
        assert update_response.status_code == status.HTTP_200_OK
        updated_data = update_response.json()
        assert updated_data["tipo"] == sample_restriccion_update_data["tipo"]
        
        # 4. UPDATE (parcial) - Actualizar parcialmente
        patch_response = authenticated_client.patch(f"/restricciones/{restriccion_id}", json=sample_restriccion_patch_data)
        assert patch_response.status_code == status.HTTP_200_OK
        patched_data = patch_response.json()
        assert patched_data["prioridad"] == sample_restriccion_patch_data["prioridad"]
        
        # 5. READ ALL - Verificar que aparece en la lista
        list_response = authenticated_client.get("/restricciones/")
        assert list_response.status_code == status.HTTP_200_OK
        restricciones = list_response.json()
        assert len(restricciones) == 1
        assert restricciones[0]["id"] == restriccion_id
        
        # 6. DELETE - Eliminar restricción
        delete_response = authenticated_client.delete(f"/restricciones/{restriccion_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # 7. VERIFY DELETE - Verificar que fue eliminada
        final_get_response = authenticated_client.get(f"/restricciones/{restriccion_id}")
        assert final_get_response.status_code == status.HTTP_404_NOT_FOUND
        
        # 8. VERIFY EMPTY LIST - Verificar que la lista está vacía
        final_list_response = authenticated_client.get("/restricciones/")
        assert final_list_response.status_code == status.HTTP_200_OK
        assert final_list_response.json() == []

    def test_multiple_restricciones_management(self, authenticated_client, sample_restriccion_data):
        """Prueba gestión de múltiples restricciones"""
        sample_restriccion_data["docente_id"] = self.docente_id
        created_ids = []
        tipos_validos = ["horario", "aula", "materia"]
        
        # Crear múltiples restricciones
        for i in range(3):
            data = sample_restriccion_data.copy()
            data["tipo"] = tipos_validos[i]
            data["valor"] = f"valor_{i}"
            data["prioridad"] = i + 1
            
            response = authenticated_client.post("/restricciones/", json=data)
            assert response.status_code == status.HTTP_201_CREATED
            created_ids.append(response.json()["id"])
        
        # Verificar que todas aparecen en la lista
        list_response = authenticated_client.get("/restricciones/")
        assert list_response.status_code == status.HTTP_200_OK
        restricciones = list_response.json()
        assert len(restricciones) == 3
        
        # Verificar IDs únicos
        response_ids = [r["id"] for r in restricciones]
        assert set(response_ids) == set(created_ids)
        
        # Eliminar una restricción
        delete_response = authenticated_client.delete(f"/restricciones/{created_ids[1]}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que quedan solo 2
        final_list_response = authenticated_client.get("/restricciones/")
        assert final_list_response.status_code == status.HTTP_200_OK
        assert len(final_list_response.json()) == 2
