from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from domain.entities import EstudianteCreate
from domain.models import Estudiante


class SQLEstudianteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, estudiante: EstudianteCreate) -> Estudiante:
        """Crear un nuevo estudiante"""
        db_estudiante = Estudiante(user_id=estudiante.user_id, matricula=estudiante.matricula)
        self.session.add(db_estudiante)
        self.session.commit()
        self.session.refresh(db_estudiante)
        return db_estudiante

    def get_by_id(self, estudiante_id: int) -> Optional[Estudiante]:
        """Obtener estudiante por ID"""
        return (
            self.session.query(Estudiante)
            .options(joinedload(Estudiante.user))
            .filter(Estudiante.id == estudiante_id)
            .first()
        )

    def get_by_user_id(self, user_id: int) -> Optional[Estudiante]:
        """Obtener estudiante por user_id"""
        return (
            self.session.query(Estudiante)
            .options(joinedload(Estudiante.user))
            .filter(Estudiante.user_id == user_id)
            .first()
        )

    def get_by_matricula(self, matricula: str) -> Optional[Estudiante]:
        """Obtener estudiante por matrícula"""
        return (
            self.session.query(Estudiante)
            .options(joinedload(Estudiante.user))
            .filter(Estudiante.matricula == matricula)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        """Obtener todos los estudiantes con paginación"""
        return (
            self.session.query(Estudiante)
            .options(joinedload(Estudiante.user))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete(self, estudiante_id: int) -> bool:
        """Eliminar un estudiante"""
        db_estudiante = self.get_by_id(estudiante_id)
        if db_estudiante:
            self.session.delete(db_estudiante)
            self.session.commit()
            return True
        return False
