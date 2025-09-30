from typing import List
from fastapi import HTTPException, status
from domain.entities import Campus, CampusCreate
from infrastructure.repositories.campus_repository import SQLCampusRepository

class CampusUseCase:
    def __init__(self, campus_repository: SQLCampusRepository):
        self.campus_repository = campus_repository

    def create_campus(self, campus_data: CampusCreate) -> Campus:
        """Crear un nuevo campus"""
        # Verificar que no exista un campus con el mismo nombre
        existing_campus = self.campus_repository.get_by_nombre(campus_data.nombre)
        if existing_campus:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un campus con el nombre '{campus_data.nombre}'"
            )
        
        return self.campus_repository.create(campus_data)

    def get_all_campus(self) -> List[Campus]:
        """Obtener todos los campus"""
        campus = self.campus_repository.get_all()
        if not campus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay campus registrados"
            )
        return campus

    def get_campus_by_id(self, campus_id: int) -> Campus:
        """Obtener campus por ID"""
        campus = self.campus_repository.get_by_id(campus_id)
        if not campus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campus con id {campus_id} no encontrado"
            )
        return campus

    def delete_campus(self, campus_id: int) -> bool:
        """Eliminar un campus"""
        campus = self.campus_repository.get_by_id(campus_id)
        if not campus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campus con id {campus_id} no encontrado"
            )
        
        return self.campus_repository.delete(campus_id)