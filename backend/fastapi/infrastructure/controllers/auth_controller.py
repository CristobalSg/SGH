from fastapi import APIRouter, Depends, HTTPException, status
from domain.entities import UserCreate, User, UserLogin, Token, TokenResponse, RefreshTokenRequest
from domain.authorization import Permission  # ✅ MIGRADO
from infrastructure.dependencies import get_user_auth_use_case, require_permission  # ✅ MIGRADO
from application.use_cases.user_auth_use_cases import UserAuthUseCase

router = APIRouter()

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario (Solo Admin)",
    description="Crea un nuevo usuario en el sistema. **Requiere permisos de administrador (USER:CREATE)**"
)
async def register(
    user_data: UserCreate,
    current_user: User = Depends(require_permission(Permission.USER_CREATE)),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Registrar un nuevo usuario (requiere permiso USER:CREATE - solo administradores)"""
    try:
        user = auth_use_case.register_user(user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Iniciar sesión y obtener token de acceso"""
    try:
        token = auth_use_case.login_user_token_only(login_data)
        return token
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login-json", response_model=TokenResponse)
async def login_json(
    login_data: UserLogin,
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Iniciar sesión con JSON y obtener token de acceso"""
    try:
        token = auth_use_case.login_user_token_only(login_data)
        return token
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(require_permission(Permission.USER_READ))  # ✅ MIGRADO
):
    """Obtener información del usuario actual (requiere permiso USER:READ)"""
    return current_user

@router.get("/me/detailed")
async def read_users_me_detailed(
    current_user: User = Depends(require_permission(Permission.USER_READ)),  # ✅ MIGRADO
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Obtener información detallada del usuario actual incluyendo datos específicos del rol (requiere permiso USER:READ)"""
    return auth_use_case.get_user_specific_data(current_user)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Refrescar access token usando refresh token"""
    try:
        new_token = auth_use_case.refresh_access_token_only(refresh_request)
        return new_token
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# ============================================================================
# ENDPOINTS DE VALIDACIÓN DE ROLES - TEMPORALMENTE COMENTADOS
# ============================================================================
# NOTA DE SEGURIDAD: Estos endpoints exponen información sensible sobre roles
# Serán reemplazados por un sistema de logging de auditoría en el futuro
# Por ahora, la validación de roles debe hacerse usando las dependencies:
# - get_current_admin_user
# - get_current_docente_user  
# - get_current_estudiante_user
# - get_current_docente_or_admin_user
# ============================================================================

# @router.get("/validate-role/{required_role}")
# async def validate_user_role(
#     required_role: str,
#     current_user: User = Depends(get_current_active_user),
#     auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
# ):
#     """[DESHABILITADO] Validar si el usuario actual tiene el rol requerido
#     
#     Este endpoint ha sido deshabilitado por razones de seguridad.
#     Expone información sensible sobre la estructura de roles del sistema.
#     Use las dependencies de FastAPI para validación de roles en el backend.
#     """
#     # TODO: Implementar logging de auditoría antes de reactivar
#     try:
#         has_role = auth_use_case.require_role(current_user, [required_role])
#         # No retornar información de roles
#         return {"valid": has_role}
#     except HTTPException:
#         return {"valid": False}

# @router.get("/validate-admin")
# async def validate_admin(
#     current_user: User = Depends(get_current_active_user),
#     auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
# ):
#     """[DESHABILITADO] Validar si el usuario actual es administrador
#     
#     Este endpoint ha sido deshabilitado por razones de seguridad.
#     Use get_current_admin_user dependency en los endpoints que lo requieran.
#     """
#     # TODO: Implementar logging de auditoría antes de reactivar
#     try:
#         is_admin = auth_use_case.require_admin(current_user)
#         return {"valid": is_admin}
#     except HTTPException:
#         return {"valid": False}

# @router.get("/validate-docente")
# async def validate_docente(
#     current_user: User = Depends(get_current_active_user),
#     auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
# ):
#     """[DESHABILITADO] Validar si el usuario actual es docente
#     
#     Este endpoint ha sido deshabilitado por razones de seguridad.
#     Use get_current_docente_user dependency en los endpoints que lo requieran.
#     """
#     # TODO: Implementar logging de auditoría antes de reactivar
#     try:
#         is_docente = auth_use_case.require_docente(current_user)
#         return {"valid": is_docente}
#     except HTTPException:
#         return {"valid": False}

# @router.get("/validate-estudiante")
# async def validate_estudiante(
#     current_user: User = Depends(get_current_active_user),
#     auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
# ):
#     """[DESHABILITADO] Validar si el usuario actual es estudiante
#     
#     Este endpoint ha sido deshabilitado por razones de seguridad.
#     Use get_current_estudiante_user dependency en los endpoints que lo requieran.
#     """
#     # TODO: Implementar logging de auditoría antes de reactivar
#     try:
#         is_estudiante = auth_use_case.require_estudiante(current_user)
#         return {"valid": is_estudiante}
#     except HTTPException:
#         return {"valid": False}

# @router.get("/validate-docente-or-admin")
# async def validate_docente_or_admin(
#     current_user: User = Depends(get_current_active_user),
#     auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
# ):
#     """[DESHABILITADO] Validar si el usuario actual es docente o administrador
#     
#     Este endpoint ha sido deshabilitado por razones de seguridad.
#     Use get_current_docente_or_admin_user dependency en los endpoints que lo requieran.
#     """
#     # TODO: Implementar logging de auditoría antes de reactivar
#     try:
#         is_docente_or_admin = auth_use_case.require_docente_or_admin(current_user)
#         return {"valid": is_docente_or_admin}
#     except HTTPException:
#         return {"valid": False}