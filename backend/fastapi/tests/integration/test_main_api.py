import pytest
from fastapi import status


class TestMainIntegration:
    """Pruebas de integración para los endpoints principales"""

    def test_root_endpoint(self, client):
        """Prueba GET / para obtener información básica del API"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "SGH Backend API"
        assert data["version"] == "0.1.0"
        assert "environment" in data

    def test_health_endpoint(self, client):
        """Prueba GET /health para verificar el estado del sistema"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "environment" in data