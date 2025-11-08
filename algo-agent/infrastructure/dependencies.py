from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from domain.entities import User
from domain.authorization import Permission, UserRole
from application.use_cases.user_auth_use_cases import UserAuthUseCase

from application.services.authorization_service import AuthorizationService

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


def require_permission(permission: Permission) -> Callable:
    """
    Factory de dependency para requerir un permiso específico.
    
    Uso:
        @router.delete("/users/{user_id}")
        async def delete_user(
            user_id: int,
            current_user: User = Depends(require_permission(Permission.USER_DELETE))
        ):
            ...
    
    Args:
        permission: Permiso requerido
        
    Returns:
        Dependency function que verifica el permiso
    """
    def permission_dependency(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        AuthorizationService.verify_permission(current_user, permission)
        return current_user
    
    return permission_dependency


def require_any_permission(*permissions: Permission) -> Callable:
    """
    Factory de dependency para requerir al menos uno de varios permisos.
    
    Uso:
        @router.get("/restricciones")
        async def get_restricciones(
            user: User = Depends(require_any_permission(
                Permission.RESTRICCION_READ,
                Permission.RESTRICCION_READ_OWN
            ))
        ):
            ...
    
    Args:
        *permissions: Permisos (requiere al menos uno)
        
    Returns:
        Dependency function que verifica los permisos
    """
    def permission_dependency(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        AuthorizationService.verify_any_permission(current_user, list(permissions))
        return current_user
    
    return permission_dependency


def require_role(role: UserRole) -> Callable:
    """
    Factory de dependency para requerir un rol específico.
    
    Uso:
        @router.get("/admin/settings")
        async def admin_settings(
            current_user: User = Depends(require_role(UserRole.ADMINISTRADOR))
        ):
            ...
    
    Args:
        role: Rol requerido
        
    Returns:
        Dependency function que verifica el rol
    """
    def role_dependency(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        AuthorizationService.verify_role(current_user, role)
        return current_user
    
    return role_dependency


def require_any_role(*roles: UserRole) -> Callable:
    """
    Factory de dependency para requerir uno de varios roles.
    
    Uso:
        @router.get("/restricciones")
        async def get_restricciones(
            user: User = Depends(require_any_role(
                UserRole.ADMINISTRADOR,
                UserRole.DOCENTE
            ))
        ):
            ...
    
    Args:
        *roles: Roles válidos (requiere al menos uno)
        
    Returns:
        Dependency function que verifica los roles
    """
    def role_dependency(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        AuthorizationService.verify_any_role(current_user, list(roles))
        return current_user
    
    return role_dependency