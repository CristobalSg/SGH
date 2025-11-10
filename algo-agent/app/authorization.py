"""
Compact authorization helpers that keep the original business rules
without spreading them across domain/application layers.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional, Set

from fastapi import HTTPException, status

from app.schemas import User


class UserRole(str, Enum):
    ADMINISTRADOR = "administrador"
    DOCENTE = "docente"
    ESTUDIANTE = "estudiante"

    @classmethod
    def values(cls) -> List[str]:
        return [role.value for role in cls]


class Permission(str, Enum):
    USER_READ = "user:read"
    USER_READ_ALL = "user:read:all"
    USER_CREATE = "user:create"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    USER_ACTIVATE = "user:activate"

    DOCENTE_READ = "docente:read"
    DOCENTE_WRITE = "docente:write"
    DOCENTE_DELETE = "docente:delete"

    ESTUDIANTE_READ = "estudiante:read"
    ESTUDIANTE_WRITE = "estudiante:write"
    ESTUDIANTE_DELETE = "estudiante:delete"

    ASIGNATURA_READ = "asignatura:read"
    ASIGNATURA_WRITE = "asignatura:write"
    ASIGNATURA_DELETE = "asignatura:delete"

    SECCION_READ = "seccion:read"
    SECCION_WRITE = "seccion:write"
    SECCION_DELETE = "seccion:delete"

    SALA_READ = "sala:read"
    SALA_WRITE = "sala:write"
    SALA_DELETE = "sala:delete"

    CAMPUS_READ = "campus:read"
    CAMPUS_WRITE = "campus:write"
    CAMPUS_DELETE = "campus:delete"

    EDIFICIO_READ = "edificio:read"
    EDIFICIO_WRITE = "edificio:write"
    EDIFICIO_DELETE = "edificio:delete"

    RESTRICCION_READ = "restriccion:read"
    RESTRICCION_READ_OWN = "restriccion:read:own"
    RESTRICCION_READ_ALL = "restriccion:read:all"
    RESTRICCION_WRITE = "restriccion:write"
    RESTRICCION_WRITE_OWN = "restriccion:write:own"
    RESTRICCION_DELETE = "restriccion:delete"
    RESTRICCION_DELETE_OWN = "restriccion:delete:own"

    RESTRICCION_HORARIO_READ = "restriccion_horario:read"
    RESTRICCION_HORARIO_READ_OWN = "restriccion_horario:read:own"
    RESTRICCION_HORARIO_READ_ALL = "restriccion_horario:read:all"
    RESTRICCION_HORARIO_WRITE = "restriccion_horario:write"
    RESTRICCION_HORARIO_WRITE_OWN = "restriccion_horario:write:own"
    RESTRICCION_HORARIO_DELETE = "restriccion_horario:delete"
    RESTRICCION_HORARIO_DELETE_OWN = "restriccion_horario:delete:own"

    HORARIO_WRITE = "horario:write"
    HORARIO_READ = "horario:read"

    CLASE_READ = "clase:read"
    CLASE_WRITE = "clase:write"
    CLASE_DELETE = "clase:delete"

    BLOQUE_READ = "bloque:read"
    BLOQUE_WRITE = "bloque:write"
    BLOQUE_DELETE = "bloque:delete"

    SYSTEM_CONFIG = "system:config"
    SYSTEM_LOGS = "system:logs"


ROLE_PERMISSIONS: Dict[UserRole, Set[Permission]] = {
    UserRole.ADMINISTRADOR: set(item for item in Permission),
    UserRole.DOCENTE: {
        Permission.USER_READ,
        Permission.DOCENTE_READ,
        Permission.ASIGNATURA_READ,
        Permission.SECCION_READ,
        Permission.SALA_READ,
        Permission.CAMPUS_READ,
        Permission.EDIFICIO_READ,
        Permission.CLASE_READ,
        Permission.BLOQUE_READ,
        Permission.RESTRICCION_READ_OWN,
        Permission.RESTRICCION_WRITE_OWN,
        Permission.RESTRICCION_DELETE_OWN,
        Permission.RESTRICCION_HORARIO_READ_OWN,
        Permission.RESTRICCION_HORARIO_WRITE_OWN,
        Permission.RESTRICCION_HORARIO_DELETE_OWN,
        Permission.HORARIO_READ,
    },
    UserRole.ESTUDIANTE: {
        Permission.USER_READ,
        Permission.ESTUDIANTE_READ,
        Permission.ASIGNATURA_READ,
        Permission.SECCION_READ,
        Permission.SALA_READ,
        Permission.CAMPUS_READ,
        Permission.EDIFICIO_READ,
        Permission.CLASE_READ,
        Permission.BLOQUE_READ,
        Permission.HORARIO_READ,
    },
}


@dataclass
class AccessRule:
    resource_type: str
    action: str
    requires_ownership: bool = False
    custom_validator: Optional[Callable] = None
    description: str = ""


class AuthorizationRules:
    @staticmethod
    def can_access_user_data(actor_role: UserRole, actor_id: int, target_user_id: int) -> bool:
        if actor_role == UserRole.ADMINISTRADOR:
            return True
        return actor_id == target_user_id

    @staticmethod
    def can_modify_restriccion(
        actor_role: UserRole, actor_docente_id: Optional[int], restriccion_docente_id: int
    ) -> bool:
        if actor_role == UserRole.ADMINISTRADOR:
            return True
        if actor_role == UserRole.DOCENTE:
            return actor_docente_id == restriccion_docente_id
        return False

    @staticmethod
    def can_list_all_users(actor_role: UserRole) -> bool:
        return actor_role == UserRole.ADMINISTRADOR


class PermissionChecker:
    @staticmethod
    def has_permission(user_role: UserRole, permission: Permission) -> bool:
        return permission in ROLE_PERMISSIONS.get(user_role, set())

    @staticmethod
    def has_any_permission(user_role: UserRole, permissions: List[Permission]) -> bool:
        return any(permission in ROLE_PERMISSIONS.get(user_role, set()) for permission in permissions)

    @staticmethod
    def has_all_permissions(user_role: UserRole, permissions: List[Permission]) -> bool:
        role_permissions = ROLE_PERMISSIONS.get(user_role, set())
        return all(permission in role_permissions for permission in permissions)


class AuthorizationService:
    @staticmethod
    def verify_permission(user: User, permission: Permission) -> None:
        role = UserRole(user.rol)
        if not PermissionChecker.has_permission(role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado: se requiere '{permission.value}'",
            )

    @staticmethod
    def verify_any_permission(user: User, permissions: List[Permission]) -> None:
        role = UserRole(user.rol)
        if not PermissionChecker.has_any_permission(role, permissions):
            perms = "', '".join(p.value for p in permissions)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado: se requiere uno de: '{perms}'",
            )

    @staticmethod
    def verify_all_permissions(user: User, permissions: List[Permission]) -> None:
        role = UserRole(user.rol)
        if not PermissionChecker.has_all_permissions(role, permissions):
            perms = "', '".join(p.value for p in permissions)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado: se requieren todos: '{perms}'",
            )

    @staticmethod
    def verify_role(user: User, required_role: UserRole) -> None:
        if user.rol != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: se requiere rol '{required_role.value}'",
            )

    @staticmethod
    def verify_any_role(user: User, required_roles: List[UserRole]) -> None:
        if user.rol not in [role.value for role in required_roles]:
            roles = "', '".join(role.value for role in required_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: se requiere uno de los roles: '{roles}'",
            )


__all__ = [
    "UserRole",
    "Permission",
    "AuthorizationRules",
    "AuthorizationService",
    "PermissionChecker",
]
