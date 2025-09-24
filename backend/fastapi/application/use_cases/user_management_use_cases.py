from typing import List
from fastapi import HTTPException, status
from domain.entities import User
from infrastructure.repositories.user_repository import SQLUserRepository

class UserManagementUseCase:
    def __init__(self, user_repository: SQLUserRepository):
        self.user_repository = user_repository

    def get_all_users(self) -> List[User]:
        users = self.user_repository.get_all()
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
