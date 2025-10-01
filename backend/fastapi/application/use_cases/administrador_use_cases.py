from typing import List
from fastapi import HTTPException, status
from domain.entities import Administrador, AdministradorCreate
from infrastructure.repositories.administrador_repository import SQLAdministradorRepository
from infrastructure.repositories.user_repository import SQLUserRepository

class AdministradorUseCase:
    def __init__(self, administrador_repository: SQLAdministradorRepository, user_repository: SQLUserRepository):
        self.administrador_repository = administrador_repository
        self.user_repository = user_repository

    def create_administrador(self, administrador_data: AdministradorCreate) -> Administrador:
        """Crear un nuevo administrador"""
        # Verificar que el usuario existe y tiene rol de administrador
        user = self.user_repository.get_by_id(administrador_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {administrador_data.user_id} no encontrado"
            )
        
        if user.rol != 'administrador':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario debe tener rol de administrador"
            )
        
        # Verificar que no exista ya un administrador para este usuario
        existing_administrador = self.administrador_repository.get_by_user_id(administrador_data.user_id)
        if existing_administrador:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un administrador asociado al usuario {administrador_data.user_id}"
            )
        
        return self.administrador_repository.create(administrador_data)

    def get_all_administradores(self) -> List[Administrador]:
        """Obtener todos los administradores"""
        administradores = self.administrador_repository.get_all()
        if not administradores:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay administradores registrados"
            )
        return administradores

    def get_administrador_by_id(self, administrador_id: int) -> Administrador:
        """Obtener administrador por ID"""
        administrador = self.administrador_repository.get_by_id(administrador_id)
        if not administrador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Administrador con id {administrador_id} no encontrado"
            )
        return administrador

    def delete_administrador(self, administrador_id: int) -> bool:
        """Eliminar un administrador"""
        administrador = self.administrador_repository.get_by_id(administrador_id)
        if not administrador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Administrador con id {administrador_id} no encontrado"
            )
        
        return self.administrador_repository.delete(administrador_id)