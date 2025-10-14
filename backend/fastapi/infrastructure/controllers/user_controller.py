from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from typing import List
from domain.entities import User, UserUpdate
from infrastructure.dependencies import get_user_management_use_case, get_current_active_user, get_current_admin_user
from application.use_cases.user_management_use_cases import UserManagementUseCase

router = APIRouter()

@router.get("/", response_model=List[User], summary="Obtener todos los usuarios")
async def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener todos los usuarios con paginación (requiere autenticación)"""
    try:
        users = user_use_case.get_all_users(skip=skip, limit=limit)
        return users
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/{user_id}", response_model=User, summary="Obtener usuario por ID")
async def get_user_by_id(
    user_id: int = Path(..., gt=0, description="ID del usuario"),
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un usuario por ID (requiere autenticación)"""
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

@router.get("/email/{email}", response_model=User, summary="Obtener usuario por email")
async def get_user_by_email(
    email: str = Path(..., description="Email del usuario"),
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_admin_user)
):
    """Obtener un usuario por email (solo administradores)"""
    try:
        user = user_use_case.get_user_by_email(email)
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/rol/{rol}", response_model=List[User], summary="Obtener usuarios por rol")
async def get_users_by_rol(
    rol: str = Path(..., description="Rol del usuario (administrador, docente, estudiante)"),
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_admin_user)
):
    """Obtener todos los usuarios con un rol específico (solo administradores)"""
    try:
        users = user_use_case.get_users_by_rol(rol)
        return users
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="Actualizar usuario")
async def update_user(
    user_id: int = Path(..., gt=0, description="ID del usuario"),
    user_data: UserUpdate = None,
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_admin_user)
):
    """Actualizar información de un usuario (solo administradores)"""
    try:
        updated_user = user_use_case.update_user(user_id, user_data)
        return updated_user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario")
async def delete_user(
    user_id: int = Path(..., gt=0, description="ID del usuario"),
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_admin_user)
):
    """Eliminar un usuario (solo administradores)"""
    try:
        user_use_case.delete_user(user_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.patch("/{user_id}/activate", response_model=User, status_code=status.HTTP_200_OK, summary="Activar usuario")
async def activate_user(
    user_id: int = Path(..., gt=0, description="ID del usuario"),
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_admin_user)
):
    """Activar un usuario (solo administradores)"""
    try:
        activated_user = user_use_case.activate_user(user_id)
        return activated_user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.patch("/{user_id}/deactivate", response_model=User, status_code=status.HTTP_200_OK, summary="Desactivar usuario")
async def deactivate_user(
    user_id: int = Path(..., gt=0, description="ID del usuario"),
    user_use_case: UserManagementUseCase = Depends(get_user_management_use_case),
    current_user: User = Depends(get_current_admin_user)
):
    """Desactivar un usuario (solo administradores)"""
    try:
        deactivated_user = user_use_case.deactivate_user(user_id)
        return deactivated_user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
