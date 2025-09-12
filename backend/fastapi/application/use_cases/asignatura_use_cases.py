from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import AsignaturaCreate, Asignatura
from infrastructure.repositories.asignatura_repository import AsignaturaRepository

class AsignaturaUseCases:
    def __init__(self, asignatura_repository: AsignaturaRepository):
        self.asignatura_repository = asignatura_repository

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Asignatura]:
        """Obtener todas las asignaturas con paginación"""
        return self.asignatura_repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, asignatura_id: int) -> Asignatura:
        """Obtener asignatura por ID"""
        asignatura = self.asignatura_repository.get_by_id(asignatura_id)
        if not asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asignatura no encontrada"
            )
        return asignatura

    def get_by_codigo(self, codigo: str) -> Asignatura:
        """Obtener asignatura por código"""
        asignatura = self.asignatura_repository.get_by_codigo(codigo)
        if not asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asignatura no encontrada"
            )
        return asignatura

    def create(self, asignatura_data: AsignaturaCreate) -> Asignatura:
        """Crear una nueva asignatura"""
        # Verificar si el código ya existe
        existing_asignatura = self.asignatura_repository.get_by_codigo(asignatura_data.codigo)
        if existing_asignatura:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de asignatura ya existe"
            )
        
        return self.asignatura_repository.create(asignatura_data)

    def update(self, asignatura_id: int, **update_data) -> Asignatura:
        """Actualizar una asignatura"""
        # Verificar que la asignatura existe
        existing_asignatura = self.asignatura_repository.get_by_id(asignatura_id)
        if not existing_asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asignatura no encontrada"
            )
        
        # Si se actualiza el código, verificar que no exista otra asignatura con ese código
        if 'codigo' in update_data:
            asignatura_with_codigo = self.asignatura_repository.get_by_codigo(update_data['codigo'])
            if asignatura_with_codigo and asignatura_with_codigo.id != asignatura_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código ya está registrado por otra asignatura"
                )
        
        updated_asignatura = self.asignatura_repository.update(asignatura_id, update_data)
        if not updated_asignatura:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la asignatura"
            )
        return updated_asignatura

    def delete(self, asignatura_id: int) -> bool:
        """Eliminar una asignatura"""
        # Verificar que la asignatura existe
        existing_asignatura = self.asignatura_repository.get_by_id(asignatura_id)
        if not existing_asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asignatura no encontrada"
            )
        
        # Verificar si tiene secciones asociadas
        if self.asignatura_repository.has_secciones(asignatura_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar la asignatura porque tiene secciones asociadas"
            )
        
        success = self.asignatura_repository.delete(asignatura_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la asignatura"
            )
        return success

    def search_by_nombre(self, nombre: str) -> List[Asignatura]:
        """Buscar asignaturas por nombre"""
        return self.asignatura_repository.search_by_nombre(nombre)

    def get_by_creditos(self, creditos_min: int = None, creditos_max: int = None) -> List[Asignatura]:
        """Obtener asignaturas por rango de créditos"""
        return self.asignatura_repository.get_by_creditos(creditos_min, creditos_max)