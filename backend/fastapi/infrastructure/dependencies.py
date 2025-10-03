from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from domain.entities import User
from infrastructure.database.config import get_db
from infrastructure.repositories.user_repository import SQLUserRepository
from application.use_cases.user_management_use_cases import UserManagementUseCase
from application.use_cases.user_auth_use_cases import UserAuthUseCase

def get_user_repository(db: Session = Depends(get_db)) -> SQLUserRepository:
    """Dependency para obtener el repositorio de usuarios"""
    return SQLUserRepository(db)

def get_user_auth_use_case(
    user_repository: SQLUserRepository = Depends(get_user_repository)
) -> UserAuthUseCase:
    """Dependency para obtener el caso de uso de autenticación"""
    return UserAuthUseCase(user_repository)

def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    """Extraer token del header Authorization"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token debe ser de tipo Bearer",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Esquema de autorización inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(
    token: str = Depends(get_token_from_header),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
) -> User:
    """Dependency para obtener el usuario actual desde el token"""
    return auth_use_case.get_current_active_user(token)

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency para obtener el usuario actual activo"""
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
) -> User:
    """Dependency para obtener el usuario actual que debe ser administrador"""
    auth_use_case.require_admin(current_user)
    return current_user

def get_current_docente_user(
    current_user: User = Depends(get_current_active_user),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
) -> User:
    """Dependency para obtener el usuario actual que debe ser docente"""
    auth_use_case.require_docente(current_user)
    return current_user

def get_current_estudiante_user(
    current_user: User = Depends(get_current_active_user),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
) -> User:
    """Dependency para obtener el usuario actual que debe ser estudiante"""
    auth_use_case.require_estudiante(current_user)
    return current_user

def get_current_docente_or_admin_user(
    current_user: User = Depends(get_current_active_user),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
) -> User:
    """Dependency para obtener el usuario actual que debe ser docente o administrador"""
    auth_use_case.require_docente_or_admin(current_user)
    return current_user


def get_user_management_use_case() -> UserManagementUseCase:
    return UserManagementUseCase(SQLUserRepository())