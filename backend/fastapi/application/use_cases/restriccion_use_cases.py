from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import RestriccionCreate, Restriccion
from infrastructure.repositories.restriccion_repository import RestriccionRepository

class RestriccionUseCases:
    def __init__(self, restriccion_repository: RestriccionRepository):
        self.restriccion_repository = restriccion_repository

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Restriccion]:
        """Obtener todas las restricciones con paginación"""
        return self.restriccion_repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, restriccion_id: int) -> Restriccion:
        """Obtener restricción por ID"""
        restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        return restriccion

    def create(self, restriccion_data: RestriccionCreate) -> Restriccion:
        """Crear una nueva restricción"""
        return self.restriccion_repository.create(restriccion_data)

    def update(self, restriccion_id: int, **update_data) -> Restriccion:
        """Actualizar una restricción"""
        # Verificar que la restricción existe
        existing_restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        
        updated_restriccion = self.restriccion_repository.update(restriccion_id, update_data)
        if not updated_restriccion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la restricción"
            )
        return updated_restriccion

    def delete(self, restriccion_id: int) -> bool:
        """Eliminar una restricción"""
        # Verificar que la restricción existe
        existing_restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        
        success = self.restriccion_repository.delete(restriccion_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la restricción"
            )
        return success

    def get_by_docente(self, docente_id: int) -> List[Restriccion]:
        """Obtener restricciones de un docente específico"""
        return self.restriccion_repository.get_by_docente(docente_id)

    def get_by_tipo(self, tipo: str) -> List[Restriccion]:
        """Obtener restricciones por tipo"""
        return self.restriccion_repository.get_by_tipo(tipo)

    def get_by_prioridad(self, prioridad_min: int = None, prioridad_max: int = None) -> List[Restriccion]:
        """Obtener restricciones por rango de prioridad"""
        return self.restriccion_repository.get_by_prioridad(prioridad_min, prioridad_max)

    def delete_by_docente(self, docente_id: int) -> int:
        """Eliminar todas las restricciones de un docente"""
        return self.restriccion_repository.delete_by_docente(docente_id)
