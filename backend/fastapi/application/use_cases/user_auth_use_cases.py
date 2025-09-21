from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from domain.entities import UserCreate, User, UserLogin, Token, RefreshTokenRequest
from infrastructure.repositories.user_repository import SQLUserRepository
from infrastructure.auth import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

class UserAuthUseCase:
    def __init__(self, user_repository: SQLUserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: UserCreate) -> User:
        """Registrar un nuevo usuario"""
        # Verificar si el email ya existe
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear el usuario
        new_user = self.user_repository.create(user_data)
        return new_user

    def login_user(self, login_data: UserLogin) -> Token:
        """Autenticar usuario y generar token"""
        # Autenticar usuario
        user = self.user_repository.authenticate(login_data.email, login_data.contrasena)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar si el usuario está activo
        if not self.user_repository.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        # Crear tokens de acceso y refresh
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        access_token = AuthService.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        refresh_token = AuthService.create_refresh_token(
            data={"sub": user.email}, expires_delta=refresh_token_expires
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # En segundos
            user=user
        )

    def get_current_user(self, token: str) -> User:
        """Obtener usuario actual desde token"""
        # Verificar token
        token_data = AuthService.verify_token(token)
        
        # Buscar usuario
        user = self.user_repository.get_by_email(token_data.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudieron validar las credenciales",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user

    def get_current_active_user(self, token: str) -> User:
        """Obtener usuario actual activo"""
        current_user = self.get_current_user(token)
        if not self.user_repository.is_active(current_user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        return current_user

    def refresh_access_token(self, refresh_token_request: RefreshTokenRequest) -> Token:
        """Generar nuevo access token usando refresh token"""
        try:
            # Verificar refresh token
            token_data = AuthService.verify_refresh_token(refresh_token_request.refresh_token)
            
            # Buscar usuario
            user = self.user_repository.get_by_email(token_data.email)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no encontrado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Verificar si el usuario está activo
            if not self.user_repository.is_active(user):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario inactivo"
                )
            
            # Crear nuevos tokens
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            
            new_access_token = AuthService.create_access_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )
            
            new_refresh_token = AuthService.create_refresh_token(
                data={"sub": user.email}, expires_delta=refresh_token_expires
            )
            
            return Token(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user=user
            )
            
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresh inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )