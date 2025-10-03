from typing import List
from fastapi import HTTPException, status
from domain.entities import Estudiante, EstudianteCreate
from infrastructure.repositories.estudiante_repository import SQLEstudianteRepository
from infrastructure.repositories.user_repository import SQLUserRepository

class EstudianteUseCase:
    def __init__(self, estudiante_repository: SQLEstudianteRepository, user_repository: SQLUserRepository):
        self.estudiante_repository = estudiante_repository
        self.user_repository = user_repository

    def create_estudiante(self, estudiante_data: EstudianteCreate) -> Estudiante:
        """Crear un nuevo estudiante"""
        # Verificar que el usuario existe y tiene rol de estudiante
        user = self.user_repository.get_by_id(estudiante_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {estudiante_data.user_id} no encontrado"
            )
        
        if user.rol != 'estudiante':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario debe tener rol de estudiante"
            )
        
        # Verificar que no exista ya un estudiante para este usuario
        existing_estudiante = self.estudiante_repository.get_by_user_id(estudiante_data.user_id)
        if existing_estudiante:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un estudiante asociado al usuario {estudiante_data.user_id}"
            )
        
        return self.estudiante_repository.create(estudiante_data)

    def get_all_estudiantes(self) -> List[Estudiante]:
        """Obtener todos los estudiantes"""
        estudiantes = self.estudiante_repository.get_all()
        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay estudiantes registrados"
            )
        return estudiantes

    def get_estudiante_by_id(self, estudiante_id: int) -> Estudiante:
        """Obtener estudiante por ID"""
        estudiante = self.estudiante_repository.get_by_id(estudiante_id)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con id {estudiante_id} no encontrado"
            )
        return estudiante

    def get_estudiante_by_matricula(self, matricula: str) -> Estudiante:
        """Obtener estudiante por matrícula"""
        estudiante = self.estudiante_repository.get_by_matricula(matricula)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con matrícula {matricula} no encontrado"
            )
        return estudiante

    def delete_estudiante(self, estudiante_id: int) -> bool:
        """Eliminar un estudiante"""
        estudiante = self.estudiante_repository.get_by_id(estudiante_id)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con id {estudiante_id} no encontrado"
            )
        
        return self.estudiante_repository.delete(estudiante_id)