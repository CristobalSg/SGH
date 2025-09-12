from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import DocenteCreate, Docente
from infrastructure.repositories.docente_repository import DocenteRepository

class DocenteUseCases:
    def __init__(self, docente_repository: DocenteRepository):
        self.docente_repository = docente_repository

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

    def create(self, docente_data: DocenteCreate) -> Docente:
        """Crear un nuevo docente"""
        # Verificar si el email ya existe
        existing_docente = self.docente_repository.get_by_email(docente_data.email)
        if existing_docente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        return self.docente_repository.create(docente_data)

    def update(self, docente_id: int, **update_data) -> Docente:
        """Actualizar un docente"""
        # Verificar que el docente existe
        existing_docente = self.docente_repository.get_by_id(docente_id)
        if not existing_docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Docente no encontrado"
            )
        
        # Si se actualiza el email, verificar que no exista otro docente con ese email
        if 'email' in update_data:
            docente_with_email = self.docente_repository.get_by_email(update_data['email'])
            if docente_with_email and docente_with_email.id != docente_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado por otro docente"
                )
        
        updated_docente = self.docente_repository.update(docente_id, update_data)
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

    def search_by_nombre(self, nombre: str) -> List[Docente]:
        """Buscar docentes por nombre"""
        return self.docente_repository.search_by_nombre(nombre)
