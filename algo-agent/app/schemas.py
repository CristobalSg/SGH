import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    rol: str
    activo: bool = Field(default=True)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, value: str) -> str:
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", value.strip()):
            raise ValueError("El nombre solo puede contener letras y espacios")
        return value.strip()

    @field_validator("rol")
    @classmethod
    def validate_rol(cls, value: str) -> str:
        roles_validos = ["docente", "estudiante", "administrador"]
        if value.lower() not in roles_validos:
            raise ValueError(f"Rol debe ser uno de: {', '.join(roles_validos)}")
        return value.lower()


class UserCreate(UserBase):
    contrasena: str = Field(..., min_length=8, max_length=100)

    @field_validator("contrasena")
    @classmethod
    def validate_contrasena(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número")
        return value


class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    activo: Optional[bool] = None


class User(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    rol: Optional[str] = None
    exp: Optional[int] = None


__all__ = [
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "TokenData",
]
