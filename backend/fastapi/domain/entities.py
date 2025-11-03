from datetime import time, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict, model_validator
import re

class UserBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    rol: str = Field(..., description="Rol del usuario (docente, estudiante, administrador)")
    activo: bool = Field(default=True, description="Estado activo del usuario")
    
    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, v):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", v.strip()):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip()
    
    @field_validator('rol')
    @classmethod
    def validate_rol(cls, v):
        roles_validos = ['docente', 'estudiante', 'administrador']
        if v.lower() not in roles_validos:
            raise ValueError(f'Rol debe ser uno de: {", ".join(roles_validos)}')
        return v.lower()

class UserCreate(UserBase):
    contrasena: str = Field(..., min_length=12, max_length=100, description="Contraseña del usuario")
    
    @field_validator('contrasena')
    @classmethod
    def validate_contrasena(cls, v):
        """
        Validar fortaleza de contraseña según OWASP:
        - Mínimo 12 caracteres
        - Al menos una letra mayúscula
        - Al menos una letra minúscula
        - Al menos un número
        - Al menos un carácter especial
        - No contraseñas comunes
        """
        # Longitud mínima
        if len(v) < 12:
            raise ValueError('La contraseña debe tener al menos 12 caracteres')
        
        # Mayúscula
        if not re.search(r"[A-Z]", v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        
        # Minúscula
        if not re.search(r"[a-z]", v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        
        # Número
        if not re.search(r"\d", v):
            raise ValueError('La contraseña debe contener al menos un número')
        
        # Carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/~`]', v):
            raise ValueError('La contraseña debe contener al menos un carácter especial (!@#$%^&*...)')
        
        # Validar contra contraseñas comunes (considerando contexto chileno y validaciones)
        # Nota: Estas contraseñas cumplen requisitos técnicos pero son predecibles
        common_passwords = [
            # Patrones comunes en español
            'password123!', 'password123@', 'password2024!', 'password2025!',
            'contrasena123!', 'contraseña123!', 'clave123!', 'clave2024!',
            'admin123!', 'admin123@', 'administrador1!', 'administrador123!',
            'usuario123!', 'usuario2024!', 'bienvenido1!', 'bienvenido123!',
            
            # Patrones chilenos comunes
            'chile123!', 'chile2024!', 'santiago123!', 'vivalchile1!',
            'chileno123!', 'chilenito1!', 'putoelqlee1!', 'weonqlio1!',
            
            # Patrones universitarios
            'estudiante1!', 'estudiante123!', 'profesor123!', 'docente123!',
            'alumno123!', 'universidad1!', 'universidad123!', 'campus123!',
            'usach123!', 'uchile123!', 'pucv123!', 'utfsm123!',
            
            # Patrones de teclado con requisitos
            'qwerty123!', 'qwerty123@', 'asdfgh123!', 'zxcvbn123!',
            'qwertyuiop1!', '1qaz2wsx3edc!', '1q2w3e4r5t!',
            
            # Nombres comunes chilenos con patrones
            'juan123!', 'maria123!', 'jose123!', 'pedro123!',
            'carmen123!', 'carlos123!', 'francisco1!', 'carolina1!',
            
            # Fechas y eventos chilenos
            '18septiembre!', '18sept2024!', 'fiestas18!', 'dieciocho1!',
            'navidad2024!', 'añonuevo2025!', 'verano2025!',
            
            # Deportes y equipos chilenos
            'colo-colo123!', 'universidad123!', 'catolica123!', 
            'chile2026!', 'laroja123!', 'futbol123!',
            
            # Patrones secuenciales que cumplen requisitos
            'abcdef123!', 'abc123def!', '123456abc!', '123abc456!',
            '1234567890ab!', 'abcd1234!', 'a1b2c3d4!',
            
            # Palabras comunes con modificaciones mínimas
            'welcome123!', 'letmein123!', 'monkey123!', 'dragon123!',
            'master123!', 'sunshine1!', 'princess1!', 'iloveyou1!',
            'baseball1!', 'football1!', 'superman1!', 'batman123!',
            
            # Patrones de sistema/testing
            'test123!', 'test2024!', 'testing123!', 'demo123!',
            'prueba123!', 'ejemplo123!', 'temporal1!', 'temp2024!',
            
            # Patrones emocionales
            'teamo123!', 'tequiero1!', 'miamor123!', 'micariño1!',
            'bebé123!', 'corazon1!', 'amor2024!',
            
            # Comida y bebidas chilenas
            'completo123!', 'empanada1!', 'terremo123!', 'piscola123!',
            'pastelchoclo1!', 'pebre123!', 'sopaipilla1!',
            
            # Lugares chilenos
            'valparaiso1!', 'concepcion1!', 'viñadelmar1!', 'temuco123!',
            'antofagasta1!', 'laserena123!', 'puertomontt1!',
            
            # Patrones repetitivos que cumplen requisitos
            'aaaaaa123!', '111111aa!', 'abcabc123!', '123123abc!',
            'password!', 'password1!', 'password12!',
        ]
        
        # Convertir a minúsculas para comparación (case-insensitive)
        if v.lower() in [p.lower() for p in common_passwords]:
            raise ValueError('La contraseña es demasiado común. Elige una más segura.')
        
        # Verificar que no sea solo caracteres repetidos
        if len(set(v)) < 6:
            raise ValueError('La contraseña no debe tener demasiados caracteres repetidos')
        
        return v

class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    activo: Optional[bool] = None

class User(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool = Field(default=True, description="Estado activo del usuario")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email del usuario")
    contrasena: str = Field(..., min_length=8, max_length=100, description="Contraseña del usuario")

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # En segundos
    user: 'User'  # Información del usuario
    rol: str  # Rol del usuario para acceso rápido

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # En segundos

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    rol: Optional[str] = None
    exp: Optional[int] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Modelo simplificado de User para mostrar en relaciones (sin datos sensibles)
class UserSimple(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool
    
    model_config = ConfigDict(from_attributes=True)

class DocenteBase(BaseModel):
    departamento: Optional[str] = Field(None, description="Departamento del docente")

class DocenteCreate(DocenteBase):
    user_id: int = Field(..., gt=0, description="ID del usuario asociado")

class Docente(DocenteBase):
    id: int
    user_id: int
    user: Optional[UserSimple] = Field(None, description="Información del usuario asociado")
    
    model_config = ConfigDict(from_attributes=True)

class EstudianteBase(BaseModel):
    matricula: Optional[str] = Field(None, description="Matrícula del estudiante")

class EstudianteCreate(EstudianteBase):
    user_id: int = Field(..., gt=0, description="ID del usuario asociado")

class Estudiante(EstudianteBase):
    id: int
    user_id: int
    user: Optional[UserSimple] = Field(None, description="Información del usuario asociado")
    
    model_config = ConfigDict(from_attributes=True)

class AdministradorBase(BaseModel):
    permisos: Optional[str] = Field(None, description="Permisos del administrador")

class AdministradorCreate(AdministradorBase):
    user_id: int = Field(..., gt=0, description="ID del usuario asociado")

class Administrador(AdministradorBase):
    id: int
    user_id: int
    user: Optional[UserSimple] = Field(None, description="Información del usuario asociado")
    
    model_config = ConfigDict(from_attributes=True)

class CampusBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del campus")
    direccion: Optional[str] = Field(None, description="Dirección del campus")

class CampusCreate(CampusBase):
    pass

class Campus(CampusBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class EdificioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del edificio")
    pisos: Optional[int] = Field(None, ge=1, description="Número de pisos")

class EdificioCreate(EdificioBase):
    campus_id: int = Field(..., gt=0, description="ID del campus")

class Edificio(EdificioBase):
    id: int
    campus_id: int
    
    model_config = ConfigDict(from_attributes=True)

class RestriccionBase(BaseModel):
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo de restricción")
    valor: str = Field(..., min_length=1, max_length=255, description="Valor de la restricción")
    prioridad: int = Field(..., ge=1, le=10, description="Prioridad de la restricción (1-10)")
    restriccion_blanda: bool = Field(default=False, description="Es restricción blanda")
    restriccion_dura: bool = Field(default=False, description="Es restricción dura")
    activa: bool = Field(default=True, description="Restricción activa")
    
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        tipos_validos = ['horario', 'aula', 'materia', 'periodo', 'disponibilidad']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo debe ser uno de: {", ".join(tipos_validos)}')
        return v.lower()
    
    @field_validator('valor')
    @classmethod
    def validate_valor(cls, v):
        if not v.strip():
            raise ValueError('El valor no puede estar vacío')
        return v.strip()

class RestriccionCreate(RestriccionBase):
    docente_id: int = Field(..., gt=0, description="ID del docente (debe ser positivo)")

class Restriccion(RestriccionBase):
    id: int
    docente_id: int
    
    model_config = ConfigDict(from_attributes=True)

class BloqueBase(BaseModel):
    dia_semana: int = Field(..., ge=0, le=6, description="Día de la semana (0=Domingo, 6=Sábado)")
    hora_inicio: time = Field(..., description="Hora de inicio del bloque")
    hora_fin: time = Field(..., description="Hora de fin del bloque")
    
    @model_validator(mode='after')
    def validate_hours(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return self
    
    @field_validator('dia_semana')
    @classmethod
    def validate_dia_semana(cls, v):
        dias_validos = [0, 1, 2, 3, 4, 5, 6]  # 0=Domingo, 1=Lunes, ..., 6=Sábado
        if v not in dias_validos:
            raise ValueError(f'Día de la semana debe estar entre 0 y 6')
        return v

class BloqueCreate(BloqueBase):
    pass

class Bloque(BloqueBase):
    id: int
    model_config = ConfigDict(
from_attributes=True)

class RestriccionHorarioBase(BaseModel):
    dia_semana: int = Field(..., ge=0, le=6, description="Día de la semana (0=Domingo, 6=Sábado)")
    hora_inicio: time = Field(..., description="Hora de inicio de la restricción")
    hora_fin: time = Field(..., description="Hora de fin de la restricción")
    disponible: bool = Field(..., description="Indica si el docente está disponible en este horario")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción opcional de la restricción")
    activa: bool = Field(default=True, description="Restricción activa")
    
    @model_validator(mode='after')
    def validate_hours(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return self
    
    @field_validator('dia_semana')
    @classmethod
    def validate_dia_semana(cls, v):
        if v not in range(0, 7):
            raise ValueError('Día de la semana debe estar entre 0 (Domingo) y 6 (Sábado)')
        return v
    
    @field_validator('descripcion')
    @classmethod
    def validate_descripcion(cls, v):
        if v is not None and not v.strip():
            return None
        return v.strip() if v else None

class RestriccionHorarioCreate(RestriccionHorarioBase):
    docente_id: int = Field(..., gt=0, description="ID del docente (debe ser positivo)")

class RestriccionHorario(RestriccionHorarioBase):
    id: int
    docente_id: int
    model_config = ConfigDict(from_attributes=True)

# ========== ASIGNATURA DTOs ==========
class AsignaturaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código de la asignatura")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la asignatura")
    creditos: int = Field(..., ge=1, le=20, description="Número de créditos (1-20)")
    
    @field_validator('codigo')
    @classmethod
    def validate_codigo(cls, v):
        if not re.match(r"^[A-Z0-9-]+$", v.strip().upper()):
            raise ValueError('El código debe contener solo letras mayúsculas, números y guiones')
        return v.strip().upper()
    
    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title()

class AsignaturaCreate(AsignaturaBase):
    pass

class Asignatura(AsignaturaBase):
    id: int
    model_config = ConfigDict(
from_attributes=True)

# ========== SECCION DTOs ==========
class SeccionBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código de la sección")
    anio: int = Field(..., ge=2020, le=2030, description="Año de la sección")
    semestre: int = Field(..., ge=1, le=2, description="Semestre (1 o 2)")
    cupos: int = Field(..., ge=1, le=100, description="Número de cupos disponibles")
    
    @field_validator('codigo')
    @classmethod
    def validate_codigo(cls, v):
        if not re.match(r"^[A-Z0-9-]+$", v.strip().upper()):
            raise ValueError('El código debe contener solo letras mayúsculas, números y guiones')
        return v.strip().upper()

class SeccionCreate(SeccionBase):
    asignatura_id: int = Field(..., gt=0, description="ID de la asignatura")

class Seccion(SeccionBase):
    id: int
    asignatura_id: int
    
    model_config = ConfigDict(from_attributes=True)

# ========== SALA DTOs ==========
class SalaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código de la sala")
    capacidad: int = Field(..., ge=1, le=500, description="Capacidad de la sala")
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo de sala")
    disponible: bool = Field(default=True, description="Disponibilidad de la sala")
    equipamiento: Optional[str] = Field(None, description="Equipamiento de la sala")
    
    @field_validator('codigo')
    @classmethod
    def validate_codigo(cls, v):
        if not re.match(r"^[A-Z0-9-]+$", v.strip().upper()):
            raise ValueError('El código debe contener solo letras mayúsculas, números y guiones')
        return v.strip().upper()
    
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        tipos_validos = ['aula', 'laboratorio', 'auditorio', 'taller', 'sala_conferencias']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo debe ser uno de: {", ".join(tipos_validos)}')
        return v.lower()

class SalaCreate(SalaBase):
    edificio_id: int = Field(..., gt=0, description="ID del edificio")

class Sala(SalaBase):
    id: int
    edificio_id: int
    model_config = ConfigDict(from_attributes=True)

# ========== CLASE DTOs ==========
class ClaseBase(BaseModel):
    estado: str = Field(..., min_length=1, max_length=20, description="Estado de la clase")
    
    @field_validator('estado')
    @classmethod
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
    
    model_config = ConfigDict(from_attributes=True)

class RestriccionPatch(BaseModel):
    """DTO para actualizaciones parciales de restricciones"""
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    valor: Optional[str] = Field(None, min_length=1, max_length=255)
    prioridad: Optional[int] = Field(None, ge=1, le=10)
    restriccion_blanda: Optional[bool] = None
    restriccion_dura: Optional[bool] = None
    activa: Optional[bool] = None
    
    @field_validator('tipo')
    @classmethod
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
    activa: Optional[bool] = None
    
    @model_validator(mode='after')
    def validate_hours(self):
        if (self.hora_fin is not None and 
            self.hora_inicio is not None and 
            self.hora_fin <= self.hora_inicio):
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return self

# ========== Patch DTOs adicionales ==========
class AsignaturaPatch(BaseModel):
    """DTO para actualizaciones parciales de asignaturas"""
    codigo: Optional[str] = Field(None, min_length=1, max_length=20)
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    creditos: Optional[int] = Field(None, ge=1, le=20)
    
    @field_validator('codigo')
    @classmethod
    def validate_codigo(cls, v):
        if v is None:
            return v
        if not re.match(r"^[A-Z0-9-]+$", v.strip().upper()):
            raise ValueError('El código debe contener solo letras mayúsculas, números y guiones')
        return v.strip().upper()

class SeccionPatch(BaseModel):
    """DTO para actualizaciones parciales de secciones"""
    codigo: Optional[str] = Field(None, min_length=1, max_length=20)
    anio: Optional[int] = Field(None, ge=2020, le=2030)
    semestre: Optional[int] = Field(None, ge=1, le=2)
    cupos: Optional[int] = Field(None, ge=1, le=100)
    asignatura_id: Optional[int] = Field(None, gt=0)

class BloquePatch(BaseModel):
    """DTO para actualizaciones parciales de bloques"""
    dia_semana: Optional[int] = Field(None, ge=0, le=6)
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    
    @model_validator(mode='after')
    def validate_hours(self):
        if (self.hora_fin is not None and 
            self.hora_inicio is not None and 
            self.hora_fin <= self.hora_inicio):
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return self

class ClasePatch(BaseModel):
    """DTO para actualizaciones parciales de clases"""
    estado: Optional[str] = Field(None, min_length=1, max_length=20)
    seccion_id: Optional[int] = Field(None, gt=0)
    docente_id: Optional[int] = Field(None, gt=0)
    sala_id: Optional[int] = Field(None, gt=0)
    bloque_id: Optional[int] = Field(None, gt=0)
    
    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v is None:
            return v
        estados_validos = ['programada', 'en_curso', 'finalizada', 'cancelada', 'suspendida']
        if v.lower() not in estados_validos:
            raise ValueError(f'Estado debe ser uno de: {", ".join(estados_validos)}')
        return v.lower()

class SalaPatch(BaseModel):
    """DTO para actualizaciones parciales de salas"""
    codigo: Optional[str] = Field(None, min_length=1, max_length=20)
    capacidad: Optional[int] = Field(None, ge=1, le=500)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    disponible: Optional[bool] = None
    equipamiento: Optional[str] = None
    edificio_id: Optional[int] = Field(None, gt=0)

class CampusPatch(BaseModel):
    """DTO para actualizaciones parciales de campus"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    direccion: Optional[str] = None

class EdificioPatch(BaseModel):
    """DTO para actualizaciones parciales de edificios"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    pisos: Optional[int] = Field(None, ge=1)
    campus_id: Optional[int] = Field(None, gt=0)

class DocentePatch(BaseModel):
    """DTO para actualizaciones parciales de docentes"""
    user_id: Optional[int] = Field(None, gt=0)
    departamento: Optional[str] = None
