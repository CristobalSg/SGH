from fastapi import APIRouter, Depends, HTTPException, status
from domain.entities import UserCreate, User, UserLogin, Token, TokenResponse, RefreshTokenRequest
from infrastructure.dependencies import get_user_auth_use_case, get_current_active_user
from application.use_cases.user_auth_use_cases import UserAuthUseCase

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Registrar un nuevo usuario"""
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
    current_user: User = Depends(get_current_active_user)
):
    """Obtener información del usuario actual"""
    return current_user

@router.get("/me/detailed")
async def read_users_me_detailed(
    current_user: User = Depends(get_current_active_user),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Obtener información detallada del usuario actual incluyendo datos específicos del rol"""
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

@router.get("/validate-role/{required_role}")
async def validate_user_role(
    required_role: str,
    current_user: User = Depends(get_current_active_user),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Validar si el usuario actual tiene el rol requerido"""
    try:
        has_role = auth_use_case.require_role(current_user, [required_role])
        return {
            "valid": has_role,
            "user_rol": current_user.rol,
            "required_role": required_role,
            "message": f"Usuario tiene el rol {current_user.rol}"
        }
    except HTTPException as e:
        return {
            "valid": False,
            "user_rol": current_user.rol,
            "required_role": required_role,
            "message": e.detail
        }