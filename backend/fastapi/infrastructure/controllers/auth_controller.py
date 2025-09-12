from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from domain.entities import UserCreate, User, UserLogin, Token
from infrastructure.database.config import get_db
from infrastructure.repositories.user_repository import SQLUserRepository
from application.use_cases.user_auth_use_cases import UserAuthUseCase

router = APIRouter()

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
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token debe ser de tipo Bearer",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return authorization.split(" ")[1]

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
    token: str = Depends(get_token_from_header),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
):
    """Obtener información del usuario actual"""
    try:
        current_user = auth_use_case.get_current_active_user(token)
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Dependency para obtener el usuario actual
async def get_current_user(
    token: str = Depends(get_token_from_header),
    auth_use_case: UserAuthUseCase = Depends(get_user_auth_use_case)
) -> User:
    """Dependency para obtener el usuario actual desde el token"""
    return auth_use_case.get_current_active_user(token)

# Dependency para obtener el usuario actual activo
async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency para obtener el usuario actual activo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user