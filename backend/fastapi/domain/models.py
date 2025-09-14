from sqlalchemy import Column, Integer, String, Time, ForeignKey, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from infrastructure.database.config import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class RestriccionHorario(Base):
    __tablename__ = "restriccion_horario"

    id = Column(Integer, primary_key=True)
    docente_id = Column(Integer, ForeignKey('docente.id'))
    dia_semana = Column(Integer)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    disponible = Column(Boolean, default=True)
    descripcion = Column(Text, nullable=True)
    
    docente = relationship("Docente", back_populates="restricciones_horario")

class Docente(Base):
    __tablename__ = "docente"

    id = Column(Integer, primary_key=True)
    nombre = Column(Text)
    email = Column(Text)
    pass_hash = Column(Text)
    
    clases = relationship("Clase", back_populates="docente")
    restricciones = relationship("Restriccion", back_populates="docente")
    restricciones_horario = relationship("RestriccionHorario", back_populates="docente")

class Asignatura(Base):
    __tablename__ = "asignatura"

    id = Column(Integer, primary_key=True)
    codigo = Column(Text)
    nombre = Column(Text)
    creditos = Column(Integer)
    
    secciones = relationship("Seccion", back_populates="asignatura")

class Seccion(Base):
    __tablename__ = "seccion"

    id = Column(Integer, primary_key=True)
    codigo = Column(Text)
    anio = Column(Integer)
    semestre = Column(Integer)
    asignatura_id = Column(Integer, ForeignKey('asignatura.id'))
    cupos = Column(Integer)
    
    asignatura = relationship("Asignatura", back_populates="secciones")
    clases = relationship("Clase", back_populates="seccion")

class Sala(Base):
    __tablename__ = "sala"

    id = Column(Integer, primary_key=True)
    codigo = Column(Text)
    capacidad = Column(Integer)
    tipo = Column(Text)
    
    clases = relationship("Clase", back_populates="sala")

class Bloque(Base):
    __tablename__ = "bloque"

    id = Column(Integer, primary_key=True)
    dia_semana = Column(Integer)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    
    clases = relationship("Clase", back_populates="bloque")

class Clase(Base):
    __tablename__ = "clase"

    id = Column(Integer, primary_key=True)
    seccion_id = Column(Integer, ForeignKey('seccion.id'))
    docente_id = Column(Integer, ForeignKey('docente.id'))
    sala_id = Column(Integer, ForeignKey('sala.id'))
    bloque_id = Column(Integer, ForeignKey('bloque.id'))
    estado = Column(Text)
    
    seccion = relationship("Seccion", back_populates="clases")
    docente = relationship("Docente", back_populates="clases")
    sala = relationship("Sala", back_populates="clases")
    bloque = relationship("Bloque", back_populates="clases")

class Restriccion(Base):
    __tablename__ = "restriccion"

    id = Column(Integer, primary_key=True)
    docente_id = Column(Integer, ForeignKey('docente.id'))
    tipo = Column(Text)
    valor = Column(Text)
    prioridad = Column(Integer)
    restriccion_blanda = Column(Text)
    restriccion_dura = Column(Text)
    
    docente = relationship("Docente", back_populates="restricciones")
