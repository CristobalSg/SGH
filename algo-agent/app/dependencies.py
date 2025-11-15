from typing import Callable, Optional

from fastapi import Depends, Header, HTTPException, status

from app.authorization import AuthorizationService, Permission, UserRole
from app.schemas import User
from app.security import AuthService
from app.settings import get_settings, AppSettings


def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        scheme, token = authorization.split()
    except ValueError as exc:  # noqa: F841
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Esquema de autorización inválido",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token debe ser de tipo Bearer",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


def get_current_user(
    token: str = Depends(get_token_from_header),
) -> User:
    token_data = AuthService.verify_token(token)
    if token_data.email is None or token_data.user_id is None or token_data.rol is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    nombre = token_data.email.split("@")[0] if token_data.email else "Usuario"
    return User(
        id=token_data.user_id,
        nombre=nombre,
        email=token_data.email,
        rol=token_data.rol,
    )


def require_permission(permission: Permission) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        AuthorizationService.verify_permission(current_user, permission)
        return current_user

    return dependency


def require_any_permission(*permissions: Permission) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        AuthorizationService.verify_any_permission(current_user, list(permissions))
        return current_user

    return dependency


def require_role(role: UserRole) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        AuthorizationService.verify_role(current_user, role)
        return current_user

    return dependency


def require_any_role(*roles: UserRole) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        AuthorizationService.verify_any_role(current_user, list(roles))
        return current_user

    return dependency


def verify_service_token(
    authorization: Optional[str] = Header(None),
    settings: AppSettings = Depends(get_settings),
) -> bool:
    """
    Valida el token de servicio para comunicación backend <-> agent.
    Usado para endpoints internos que no requieren autenticación de usuario.
    """
    if not settings.service_auth_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SERVICE_AUTH_TOKEN no configurado en el agente",
        )
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de autorización inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token debe ser de tipo Bearer",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token != settings.service_auth_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token de servicio inválido",
        )

    return True


__all__ = [
    "get_current_user",
    "get_token_from_header",
    "require_permission",
    "require_any_permission",
    "require_role",
    "require_any_role",
    "verify_service_token",
]
