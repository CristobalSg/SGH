from typing import List
from fastapi import HTTPException, status
from domain.entities import Edificio, EdificioCreate
from infrastructure.repositories.edificio_repository import SQLEdificioRepository
from infrastructure.repositories.campus_repository import SQLCampusRepository

class EdificioUseCase:
    def __init__(self, edificio_repository: SQLEdificioRepository, campus_repository: SQLCampusRepository):
        self.edificio_repository = edificio_repository
        self.campus_repository = campus_repository

    def create_edificio(self, edificio_data: EdificioCreate) -> Edificio:
        """Crear un nuevo edificio"""
        # Verificar que el campus existe
        campus = self.campus_repository.get_by_id(edificio_data.campus_id)
        if not campus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campus con id {edificio_data.campus_id} no encontrado"
            )
        
        return self.edificio_repository.create(edificio_data)

    def get_all_edificios(self) -> List[Edificio]:
        """Obtener todos los edificios"""
        edificios = self.edificio_repository.get_all()
        if not edificios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay edificios registrados"
            )
        return edificios

    def get_edificio_by_id(self, edificio_id: int) -> Edificio:
        """Obtener edificio por ID"""
        edificio = self.edificio_repository.get_by_id(edificio_id)
        if not edificio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Edificio con id {edificio_id} no encontrado"
            )
        return edificio

    def get_edificios_by_campus(self, campus_id: int) -> List[Edificio]:
        """Obtener edificios por campus"""
        # Verificar que el campus existe
        campus = self.campus_repository.get_by_id(campus_id)
        if not campus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campus con id {campus_id} no encontrado"
            )
        
        edificios = self.edificio_repository.get_by_campus(campus_id)
        if not edificios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No hay edificios en el campus {campus_id}"
            )
        return edificios

    def delete_edificio(self, edificio_id: int) -> bool:
        """Eliminar un edificio"""
        edificio = self.edificio_repository.get_by_id(edificio_id)
        if not edificio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Edificio con id {edificio_id} no encontrado"
            )
        
        return self.edificio_repository.delete(edificio_id)

    def update_edificio(self, edificio_id: int, edificio_data: EdificioCreate) -> Edificio:
        """Actualizar un edificio existente"""
        # Verificar que el edificio existe
        edificio = self.edificio_repository.get_by_id(edificio_id)
        if not edificio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Edificio con id {edificio_id} no encontrado"
            )
        
        # Verificar que el campus existe
        campus = self.campus_repository.get_by_id(edificio_data.campus_id)
        if not campus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campus con id {edificio_data.campus_id} no encontrado"
            )
        
        return self.edificio_repository.update(edificio_id, edificio_data)