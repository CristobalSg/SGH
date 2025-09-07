from datetime import time
from typing import Optional
from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class DocenteBase(BaseModel):
    nombre: str
    email: str
    pass_hash: str

class DocenteCreate(DocenteBase):
    pass

class Docente(DocenteBase):
    id: int
    class Config:
        orm_mode = True

class RestriccionBase(BaseModel):
    tipo: str
    valor: str
    prioridad: int
    restriccion_blanda: Optional[str] = None
    restriccion_dura: Optional[str] = None

class RestriccionCreate(RestriccionBase):
    docente_id: int

class Restriccion(RestriccionBase):
    id: int
    docente_id: int
    class Config:
        orm_mode = True

class BloqueBase(BaseModel):
    dia_semana: int
    hora_inicio: time
    hora_fin: time

class BloqueCreate(BloqueBase):
    pass

class Bloque(BloqueBase):
    id: int
    class Config:
        orm_mode = True
