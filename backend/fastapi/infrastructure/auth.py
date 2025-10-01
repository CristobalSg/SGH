from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from domain.entities import TokenData

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT desde variables de entorno
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key_for_development")
REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "fallback_refresh_secret_key_for_development")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "15"))  # 15 minutos
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))  # 7 días

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña es correcta"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera el hash de la contraseña"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crea un token JWT de acceso"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crea un token JWT de refresh"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> TokenData:
        """Verifica y decodifica un token JWT"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            if token_type == "access":
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            elif token_type == "refresh":
                payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            else:
                raise credentials_exception
            
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            rol: str = payload.get("rol")
            exp: int = payload.get("exp")
            token_type_payload: str = payload.get("type")
            
            if email is None or token_type_payload != token_type:
                raise credentials_exception
                
            token_data = TokenData(email=email, user_id=user_id, rol=rol, exp=exp)
            return token_data
        except JWTError:
            raise credentials_exception

    @staticmethod
    def verify_refresh_token(token: str) -> TokenData:
        """Verifica específicamente un refresh token"""
        return AuthService.verify_token(token, token_type="refresh")

    @staticmethod
    def create_tokens_for_user(user_data: dict) -> dict:
        """Crea tanto access token como refresh token para un usuario"""
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        access_token = AuthService.create_access_token(
            data=user_data, expires_delta=access_token_expires
        )
        
        refresh_token = AuthService.create_refresh_token(
            data=user_data, expires_delta=refresh_token_expires
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }