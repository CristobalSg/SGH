from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from domain.entities import User
from infrastructure.dependencies import get_user_management_use_case, get_current_active_user
from application.use_cases.user_management_use_cases import UserManagementUseCase

router = APIRouter()

@router.get("/", response_model=List[User])
async def get_users(
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener todos los usuarios (solo si estás autenticado)"""
    try:
        users = user_use_case.get_all_users()
        return users
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: int,
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un usuario por ID (solo si estás autenticado)"""
    try:
        user = user_use_case.get_user_by_id(user_id)
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
