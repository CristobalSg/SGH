import pytest
from fastapi import status


class TestTestDbIntegration:
    """Pruebas de integración para la API de test de base de datos (/db)"""

    def test_test_database_connection_success(self, client):
        """Prueba GET /db/test-db para verificar conexión a la base de datos"""
        response = client.get("/api/db/test-db")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert "Conexión a la base de datos exitosa" in data["message"]
        assert "data" in data
        assert "tablas_disponibles" in data["data"]
        
        # Verificar que las tablas esperadas están en la lista
        expected_tables = ["docente", "asignatura", "seccion", "sala", "bloque", "clase", "restriccion"]
        for table in expected_tables:
            assert table in data["data"]["tablas_disponibles"]

    def test_test_database_returns_first_docente_when_exists(self, client, db_session, sample_docente_data):
        """Prueba que el endpoint retorna el primer docente cuando existe"""
        from domain.models import Docente
        
        # Crear un docente en la base de datos
        docente = Docente(**sample_docente_data)
        db_session.add(docente)
        db_session.commit()
        db_session.refresh(docente)
        
        response = client.get("/api/db/test-db")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["primera_consulta"] is not None
        assert data["data"]["primera_consulta"]["id"] == docente.id
        assert data["data"]["primera_consulta"]["nombre"] == sample_docente_data["nombre"]

    def test_test_database_returns_null_when_no_docentes(self, client):
        """Prueba que el endpoint retorna null en primera_consulta cuando no hay docentes"""
        response = client.get("/api/db/test-db")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["primera_consulta"] is None