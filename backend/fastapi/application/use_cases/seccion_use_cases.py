from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import SeccionCreate, Seccion
from infrastructure.repositories.seccion_repository import SeccionRepository

class SeccionUseCases:
    def __init__(self, seccion_repository: SeccionRepository):
        self.seccion_repository = seccion_repository

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Seccion]:
        """Obtener todas las secciones con paginación"""
        return self.seccion_repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, seccion_id: int) -> Seccion:
        """Obtener sección por ID"""
        seccion = self.seccion_repository.get_by_id(seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        return seccion

    def create(self, seccion_data: SeccionCreate) -> Seccion:
        """Crear una nueva sección"""
        return self.seccion_repository.create(seccion_data)

    def update(self, seccion_id: int, **update_data) -> Seccion:
        """Actualizar una sección"""
        # Verificar que la sección existe
        existing_seccion = self.seccion_repository.get_by_id(seccion_id)
        if not existing_seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        
        updated_seccion = self.seccion_repository.update(seccion_id, update_data)
        if not updated_seccion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la sección"
            )
        return updated_seccion

    def delete(self, seccion_id: int) -> bool:
        """Eliminar una sección"""
        # Verificar que la sección existe
        existing_seccion = self.seccion_repository.get_by_id(seccion_id)
        if not existing_seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        
        # Verificar si tiene clases asociadas
        if self.seccion_repository.tiene_clases(seccion_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar la sección porque tiene clases asociadas"
            )
        
        success = self.seccion_repository.delete(seccion_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la sección"
            )
        return success

    def get_by_asignatura(self, asignatura_id: int) -> List[Seccion]:
        """Obtener secciones de una asignatura específica"""
        return self.seccion_repository.get_by_asignatura(asignatura_id)

    def get_by_periodo(self, anio: int, semestre: int) -> List[Seccion]:
        """Obtener secciones por año y semestre"""
        return self.seccion_repository.get_by_periodo(anio, semestre)

    def get_secciones_activas(self) -> List[Seccion]:
        """Obtener secciones activas"""
        return self.seccion_repository.get_secciones_activas()
