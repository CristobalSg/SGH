from fastapi import APIRouter, Depends, HTTPException, status
from domain.entities import UserCreate, User, UserLogin, Token, RefreshTokenRequest
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

@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Iniciar sesión y obtener token de acceso"""
    try:
        token = auth_use_case.login_user(login_data)
        return token
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login-json", response_model=Token)
async def login_json(
    login_data: UserLogin,
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Iniciar sesión con JSON y obtener token de acceso"""
    try:
        token = auth_use_case.login_user(login_data)
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

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Refrescar access token usando refresh token"""
    try:
        new_token = auth_use_case.refresh_access_token(refresh_request)
        return new_token
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )