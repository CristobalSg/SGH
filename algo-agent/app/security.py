import os
import warnings
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas import TokenData

_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=13,
    bcrypt__ident="2b",
)


def _get_secret_key(env_var: str, fallback: Optional[str]) -> str:
    env = os.getenv("NODE_ENV", "development")
    secret = os.getenv(env_var)
    if secret:
        return secret
    if env == "production":
        raise ValueError(f"La variable {env_var} debe estar configurada en producción.")
    if fallback:
        warnings.warn(
            f"Usando secret por defecto para {env_var}. Solo para desarrollo.",
            RuntimeWarning,
            stacklevel=2,
        )
        return fallback
    raise ValueError(f"Variable de entorno {env_var} no configurada")


ALLOWED_ALGORITHMS = ["HS256", "HS384", "HS512"]

SECRET_KEY = _get_secret_key("JWT_SECRET_KEY", "dev_secret_not_for_production_use")
REFRESH_SECRET_KEY = _get_secret_key(
    "JWT_REFRESH_SECRET_KEY", "dev_refresh_secret_not_for_production_use"
)
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if ALGORITHM not in ALLOWED_ALGORITHMS:
    allowed = ", ".join(ALLOWED_ALGORITHMS)
    raise ValueError(f"Algoritmo JWT no permitido: {ALGORITHM}. Usa uno de: {allowed}")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))

if SECRET_KEY == REFRESH_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY y JWT_REFRESH_SECRET_KEY deben ser diferentes.")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return _pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta if expires_delta else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_aud": False,
            "require_exp": True,
        }

        try:
            secret = SECRET_KEY if token_type == "access" else REFRESH_SECRET_KEY
            payload = jwt.decode(token, secret, algorithms=ALLOWED_ALGORITHMS, options=options)

            token_kind = payload.get("type")
            if token_kind != token_type:
                raise credentials_exception

            email: str | None = payload.get("sub")
            user_id: int | None = payload.get("user_id")
            rol: str | None = payload.get("rol")
            exp: int | None = payload.get("exp")

            if not all([email, user_id, rol, exp]):
                raise credentials_exception

            return TokenData(email=email, user_id=user_id, rol=rol, exp=exp)
        except JWTError as exc:  # noqa: F841
            raise credentials_exception

    @staticmethod
    def verify_refresh_token(token: str) -> TokenData:
        return AuthService.verify_token(token, token_type="refresh")


__all__ = [
    "AuthService",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",
]
