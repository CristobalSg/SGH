from typing import List
from fastapi import HTTPException, status
from domain.entities import User, UserUpdate
from infrastructure.repositories.user_repository import SQLUserRepository
from application.services.authorization_service import AuthorizationService  # ✅ Nuevo

class UserManagementUseCase:
    def __init__(self, user_repository: SQLUserRepository):
        self.user_repository = user_repository

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        users = self.user_repository.get_all(skip=skip, limit=limit)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay usuarios registrados"
            )
        return users

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {user_id} no encontrado"
            )
        return user

    def get_user_by_id_with_authorization(self, actor: User, user_id: int) -> User:
        """Obtener usuario por ID con verificación de acceso horizontal
        
        Args:
            actor: Usuario que realiza la solicitud
            user_id: ID del usuario a consultar
            
        Returns:
            User: Usuario solicitado
            
        Raises:
            HTTPException: 404 si no existe, 403 si no tiene acceso
        """
        # ✅ Verificar acceso horizontal usando el servicio de autorización
        AuthorizationService.verify_can_access_user(actor, user_id)
        
        # Si pasa la verificación, obtener el usuario
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {user_id} no encontrado"
            )
        return user

    def get_user_by_email(self, email: str) -> User:
        """Obtener usuario por email"""
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con email {email} no encontrado"
            )
        return user

    def get_users_by_rol(self, rol: str) -> List[User]:
        """Obtener todos los usuarios con un rol específico"""
        valid_roles = ["administrador", "docente", "estudiante"]
        if rol not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Rol inválido. Debe ser uno de: {', '.join(valid_roles)}"
            )
        
        users = self.user_repository.get_by_rol(rol)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No hay usuarios con rol {rol}"
            )
        return users

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Actualizar información de un usuario"""
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {user_id} no encontrado"
            )
        
        updated_user = self.user_repository.update(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el usuario"
            )
        return updated_user

    def delete_user(self, user_id: int) -> bool:
        """Eliminar un usuario"""
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {user_id} no encontrado"
            )
        
        success = self.user_repository.delete(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el usuario"
            )
        return success

    def activate_user(self, user_id: int) -> User:
        """Activar un usuario"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {user_id} no encontrado"
            )
        
        if user.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está activo"
            )
        
        user_update = UserUpdate(activo=True)
        return self.user_repository.update(user_id, user_update)

    def deactivate_user(self, user_id: int) -> User:
        """Desactivar un usuario"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {user_id} no encontrado"
            )
        
        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está inactivo"
            )
        
        user_update = UserUpdate(activo=False)
        return self.user_repository.update(user_id, user_update)
