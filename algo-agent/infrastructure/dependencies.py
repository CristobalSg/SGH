from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from domain.entities import User
from application.use_cases.user_auth_use_cases import UserAuthUseCase

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

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
) -> User:
    """Dependency para obtener el usuario actual que debe ser administrador"""
    auth_use_case.require_admin(current_user)
    return current_user
