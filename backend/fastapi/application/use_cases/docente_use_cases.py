from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import DocenteCreate, Docente, DocentePatch
from domain.schemas import DocenteSecureCreate, DocenteSecurePatch
from infrastructure.repositories.docente_repository import DocenteRepository
from infrastructure.repositories.user_repository import SQLUserRepository

class DocenteUseCases:
    def __init__(self, docente_repository: DocenteRepository, user_repository: SQLUserRepository):
        self.docente_repository = docente_repository
        self.user_repository = user_repository

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Docente]:
        """Obtener todos los docentes con paginación"""
        return self.docente_repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, docente_id: int) -> Docente:
        """Obtener docente por ID"""
        docente = self.docente_repository.get_by_id(docente_id)
        if not docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Docente no encontrado"
            )
        return docente

    def create(self, docente_data: DocenteSecureCreate) -> Docente:
        """Crear un nuevo docente"""
        # Verificar que el usuario existe y tiene rol de docente
        user = self.user_repository.get_by_id(docente_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {docente_data.user_id} no encontrado"
            )
        
        if user.rol != 'docente':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario debe tener rol de docente"
            )
        
        # Verificar que no exista ya un docente para este usuario
        existing_docente = self.docente_repository.get_by_user_id(docente_data.user_id)
        if existing_docente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un docente asociado al usuario {docente_data.user_id}"
            )
        
        # Convertir schema seguro a entidad
        docente_create = DocenteCreate(**docente_data.model_dump())
        return self.docente_repository.create(docente_create)

    def get_by_departamento(self, departamento: str) -> List[Docente]:
        """Obtener docentes por departamento"""
        docentes = self.docente_repository.get_by_departamento(departamento)
        if not docentes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No hay docentes en el departamento {departamento}"
            )
        return docentes

    def update(self, docente_id: int, docente_data: DocenteSecurePatch) -> Docente:
        """Actualizar parcialmente un docente"""
        # Verificar que el docente existe
        existing_docente = self.docente_repository.get_by_id(docente_id)
        if not existing_docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Docente no encontrado"
            )
        
        # Convertir schema seguro a diccionario y filtrar valores None
        update_dict = {k: v for k, v in docente_data.model_dump().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        # Actualizar usando el repositorio
        updated_docente = self.docente_repository.update(docente_id, **update_dict)
        if not updated_docente:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el docente"
            )
        
        return updated_docente

    def delete(self, docente_id: int) -> bool:
        """Eliminar un docente"""
        # Verificar que el docente existe
        existing_docente = self.docente_repository.get_by_id(docente_id)
        if not existing_docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Docente no encontrado"
            )
        
        success = self.docente_repository.delete(docente_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el docente"
            )
        return success
