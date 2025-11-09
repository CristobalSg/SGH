from datetime import time
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=8, max_length=100, description="Contraseña del usuario")

class DocenteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del docente")
    email: EmailStr = Field(..., description="Email del docente")
    pass_hash: str = Field(..., min_length=8, description="Hash de la contraseña")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", v.strip()):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip().title()

class DocenteCreate(DocenteBase):
    pass

class Docente(DocenteBase):
    id: int
    class Config:
        from_attributes = True

class RestriccionBase(BaseModel):
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo de restricción")
    valor: str = Field(..., min_length=1, max_length=255, description="Valor de la restricción")
    prioridad: int = Field(..., ge=1, le=10, description="Prioridad de la restricción (1-10)")
    restriccion_blanda: Optional[str] = Field(None, max_length=255, description="Restricción blanda opcional")
    restriccion_dura: Optional[str] = Field(None, max_length=255, description="Restricción dura opcional")
    
    @validator('tipo')
    def validate_tipo(cls, v):
        tipos_validos = ['horario', 'aula', 'materia', 'periodo', 'disponibilidad']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo debe ser uno de: {", ".join(tipos_validos)}')
        return v.lower()
    
    @validator('valor')
    def validate_valor(cls, v):
        if not v.strip():
            raise ValueError('El valor no puede estar vacío')
        return v.strip()

class RestriccionCreate(RestriccionBase):
    docente_id: int = Field(..., gt=0, description="ID del docente (debe ser positivo)")

class Restriccion(RestriccionBase):
    id: int
    docente_id: int
    class Config:
        from_attributes = True

class BloqueBase(BaseModel):
    dia_semana: int = Field(..., ge=0, le=6, description="Día de la semana (0=Domingo, 6=Sábado)")
    hora_inicio: time = Field(..., description="Hora de inicio del bloque")
    hora_fin: time = Field(..., description="Hora de fin del bloque")
    
    @validator('hora_fin')
    def validate_hora_fin(cls, v, values):
        if 'hora_inicio' in values and v <= values['hora_inicio']:
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return v
    
    @validator('dia_semana')
    def validate_dia_semana(cls, v):
        dias_validos = [0, 1, 2, 3, 4, 5, 6]  # 0=Domingo, 1=Lunes, ..., 6=Sábado
        if v not in dias_validos:
            raise ValueError(f'Día de la semana debe estar entre 0 y 6')
        return v

class BloqueCreate(BloqueBase):
    pass

class Bloque(BloqueBase):
    id: int
    class Config:
        from_attributes = True

class RestriccionHorarioBase(BaseModel):
    dia_semana: int = Field(..., ge=0, le=6, description="Día de la semana (0=Domingo, 6=Sábado)")
    hora_inicio: time = Field(..., description="Hora de inicio de la restricción")
    hora_fin: time = Field(..., description="Hora de fin de la restricción")
    disponible: bool = Field(..., description="Indica si el docente está disponible en este horario")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción opcional de la restricción")
    
    @validator('hora_fin')
    def validate_hora_fin(cls, v, values):
        if 'hora_inicio' in values and v <= values['hora_inicio']:
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return v
    
    @validator('dia_semana')
    def validate_dia_semana(cls, v):
        if v not in range(0, 7):
            raise ValueError('Día de la semana debe estar entre 0 (Domingo) y 6 (Sábado)')
        return v
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        if v is not None and not v.strip():
            return None
        return v.strip() if v else None

class RestriccionHorarioCreate(RestriccionHorarioBase):
    docente_id: int = Field(..., gt=0, description="ID del docente (debe ser positivo)")

class RestriccionHorario(RestriccionHorarioBase):
    id: int
    docente_id: int
    class Config:
        from_attributes = True

# ========== ASIGNATURA DTOs ==========
class AsignaturaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código de la asignatura")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la asignatura")
    creditos: int = Field(..., ge=1, le=20, description="Número de créditos (1-20)")
    
    @validator('codigo')
    def validate_codigo(cls, v):
        if not re.match(r"^[A-Z0-9-]+$", v.strip().upper()):
            raise ValueError('El código debe contener solo letras mayúsculas, números y guiones')
        return v.strip().upper()
    
    @validator('nombre')
    def validate_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title()

class AsignaturaCreate(AsignaturaBase):
    pass

class Asignatura(AsignaturaBase):
    id: int
    class Config:
        from_attributes = True

# ========== SECCION DTOs ==========
class SeccionBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código de la sección")
    anio: int = Field(..., ge=2020, le=2030, description="Año de la sección")
    semestre: int = Field(..., ge=1, le=2, description="Semestre (1 o 2)")
    cupos: int = Field(..., ge=1, le=100, description="Número de cupos disponibles")
    
    @validator('codigo')
    def validate_codigo(cls, v):
        if not re.match(r"^[A-Z0-9-]+$", v.strip().upper()):
            raise ValueError('El código debe contener solo letras mayúsculas, números y guiones')
        return v.strip().upper()

class SeccionCreate(SeccionBase):
    asignatura_id: int = Field(..., gt=0, description="ID de la asignatura")

class Seccion(SeccionBase):
    id: int
    asignatura_id: int
    class Config:
        from_attributes = True

# ========== SALA DTOs ==========
class SalaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código de la sala")
    capacidad: int = Field(..., ge=1, le=500, description="Capacidad de la sala")
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo de sala")
    
    @validator('codigo')
    def validate_codigo(cls, v):
        if not re.match(r"^[A-Z0-9-]+$", v.strip().upper()):
            raise ValueError('El código debe contener solo letras mayúsculas, números y guiones')
        return v.strip().upper()
    
    @validator('tipo')
    def validate_tipo(cls, v):
        tipos_validos = ['aula', 'laboratorio', 'auditorio', 'taller', 'sala_conferencias']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo debe ser uno de: {", ".join(tipos_validos)}')
        return v.lower()

class SalaCreate(SalaBase):
    pass

class Sala(SalaBase):
    id: int
    class Config:
        from_attributes = True

# ========== CLASE DTOs ==========
class ClaseBase(BaseModel):
    estado: str = Field(..., min_length=1, max_length=20, description="Estado de la clase")
    
    @validator('estado')
    def validate_estado(cls, v):
        estados_validos = ['programada', 'en_curso', 'finalizada', 'cancelada', 'suspendida']
        if v.lower() not in estados_validos:
            raise ValueError(f'Estado debe ser uno de: {", ".join(estados_validos)}')
        return v.lower()

class ClaseCreate(ClaseBase):
    seccion_id: int = Field(..., gt=0, description="ID de la sección")
    docente_id: int = Field(..., gt=0, description="ID del docente")
    sala_id: int = Field(..., gt=0, description="ID de la sala")
    bloque_id: int = Field(..., gt=0, description="ID del bloque")

class Clase(ClaseBase):
    id: int
    seccion_id: int
    docente_id: int
    sala_id: int
    bloque_id: int
    class Config:
        from_attributes = True

# ========== DTOs para operaciones complejas ==========
class RestriccionPatch(BaseModel):
    """DTO para actualizaciones parciales de restricciones"""
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    valor: Optional[str] = Field(None, min_length=1, max_length=255)
    prioridad: Optional[int] = Field(None, ge=1, le=10)
    restriccion_blanda: Optional[str] = Field(None, max_length=255)
    restriccion_dura: Optional[str] = Field(None, max_length=255)
    
    @validator('tipo')
    def validate_tipo(cls, v):
        if v is None:
            return v
        tipos_validos = ['horario', 'aula', 'materia', 'periodo', 'disponibilidad']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo debe ser uno de: {", ".join(tipos_validos)}')
        return v.lower()

class RestriccionHorarioPatch(BaseModel):
    """DTO para actualizaciones parciales de restricciones de horario"""
    dia_semana: Optional[int] = Field(None, ge=0, le=6)
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    disponible: Optional[bool] = None
    descripcion: Optional[str] = Field(None, max_length=255)
    
    @validator('hora_fin')
    def validate_hora_fin(cls, v, values):
        if v is not None and 'hora_inicio' in values and values['hora_inicio'] is not None:
            if v <= values['hora_inicio']:
                raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return v
