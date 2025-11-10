from typing import Callable, Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.authorization import AuthorizationService, Permission, UserRole
from app.database import get_db
from app.repositories import SQLUserRepository
from app.schemas import User
from app.security import AuthService


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


def get_user_repository(db: Session = Depends(get_db)) -> SQLUserRepository:
    return SQLUserRepository(db)


def get_current_user(
    token: str = Depends(get_token_from_header),
    repository: SQLUserRepository = Depends(get_user_repository),
) -> User:
    token_data = AuthService.verify_token(token)
    user = repository.get_by_email(token_data.email) if token_data.email else None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not repository.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",
        )
    return User.model_validate(user)


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


__all__ = [
    "get_current_user",
    "get_user_repository",
    "get_token_from_header",
    "require_permission",
    "require_any_permission",
    "require_role",
    "require_any_role",
]
