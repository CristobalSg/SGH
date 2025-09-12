from typing import List, Optional
from datetime import time
from sqlalchemy.orm import Session
from domain.models import RestriccionHorario
from domain.entities import RestriccionHorarioCreate

class RestriccionHorarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, restriccion: RestriccionHorarioCreate) -> RestriccionHorario:
        """Crear una nueva restricción de horario"""
        db_restriccion = RestriccionHorario(**restriccion.dict())
        self.session.add(db_restriccion)
        self.session.commit()
        self.session.refresh(db_restriccion)
        return db_restriccion

    def get_by_id(self, restriccion_id: int) -> Optional[RestriccionHorario]:
        """Obtener restricción de horario por ID"""
        return self.session.query(RestriccionHorario).filter(RestriccionHorario.id == restriccion_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[RestriccionHorario]:
        """Obtener todas las restricciones de horario con paginación"""
        return self.session.query(RestriccionHorario).offset(skip).limit(limit).all()

    def get_by_docente(self, docente_id: int) -> List[RestriccionHorario]:
        """Obtener restricciones de horario de un docente específico"""
        return self.session.query(RestriccionHorario).filter(RestriccionHorario.docente_id == docente_id).all()

    def get_by_dia_semana(self, dia_semana: int) -> List[RestriccionHorario]:
        """Obtener restricciones por día de la semana (1=Lunes, 7=Domingo)"""
        return self.session.query(RestriccionHorario).filter(RestriccionHorario.dia_semana == dia_semana).all()

    def get_by_docente_and_dia(self, docente_id: int, dia_semana: int) -> List[RestriccionHorario]:
        """Obtener restricciones de un docente en un día específico"""
        return self.session.query(RestriccionHorario).filter(
            RestriccionHorario.docente_id == docente_id,
            RestriccionHorario.dia_semana == dia_semana
        ).all()

    def get_disponibles(self, docente_id: int = None) -> List[RestriccionHorario]:
        """Obtener solo restricciones marcadas como disponibles"""
        query = self.session.query(RestriccionHorario).filter(RestriccionHorario.disponible == True)
        if docente_id:
            query = query.filter(RestriccionHorario.docente_id == docente_id)
        return query.all()

    def update(self, restriccion_id: int, restriccion_data: dict) -> Optional[RestriccionHorario]:
        """Actualizar una restricción de horario"""
        db_restriccion = self.get_by_id(restriccion_id)
        if db_restriccion:
            for key, value in restriccion_data.items():
                setattr(db_restriccion, key, value)
            self.session.commit()
            self.session.refresh(db_restriccion)
        return db_restriccion

    def delete(self, restriccion_id: int) -> bool:
        """Eliminar una restricción de horario"""
        db_restriccion = self.get_by_id(restriccion_id)
        if db_restriccion:
            self.session.delete(db_restriccion)
            self.session.commit()
            return True
        return False

    def delete_by_docente(self, docente_id: int) -> int:
        """Eliminar todas las restricciones de horario de un docente"""
        count = self.session.query(RestriccionHorario).filter(RestriccionHorario.docente_id == docente_id).count()
        self.session.query(RestriccionHorario).filter(RestriccionHorario.docente_id == docente_id).delete()
        self.session.commit()
        return count

    def get_by_docente_y_horario(self, docente_id: int, dia_semana: int, hora_inicio: time, hora_fin: time) -> List[RestriccionHorario]:
        """Verificar si existe una restricción similar para el docente en el horario dado"""
        return self.session.query(RestriccionHorario).filter(
            RestriccionHorario.docente_id == docente_id,
            RestriccionHorario.dia_semana == dia_semana,
            RestriccionHorario.hora_inicio <= hora_fin,
            RestriccionHorario.hora_fin >= hora_inicio
        ).all()

    def get_disponibilidad_docente(self, docente_id: int, dia_semana: int = None) -> List[RestriccionHorario]:
        """Obtener disponibilidad de un docente (solo restricciones marcadas como disponibles)"""
        query = self.session.query(RestriccionHorario).filter(
            RestriccionHorario.docente_id == docente_id,
            RestriccionHorario.disponible == True
        )
        if dia_semana is not None:
            query = query.filter(RestriccionHorario.dia_semana == dia_semana)
        return query.all()