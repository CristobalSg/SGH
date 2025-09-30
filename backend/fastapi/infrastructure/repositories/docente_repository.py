from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models import Docente
from domain.entities import DocenteCreate

class DocenteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, docente: DocenteCreate) -> Docente:
        """Crear un nuevo docente"""
        db_docente = Docente(
            user_id=docente.user_id,
            departamento=docente.departamento
        )
        self.session.add(db_docente)
        self.session.commit()
        self.session.refresh(db_docente)
        return db_docente

    def get_by_id(self, docente_id: int) -> Optional[Docente]:
        """Obtener docente por ID"""
        return self.session.query(Docente).filter(Docente.id == docente_id).first()

    def get_by_user_id(self, user_id: int) -> Optional[Docente]:
        """Obtener docente por user_id"""
        return self.session.query(Docente).filter(Docente.user_id == user_id).first()

    def get_by_departamento(self, departamento: str) -> List[Docente]:
        """Obtener docentes por departamento"""
        return self.session.query(Docente).filter(Docente.departamento == departamento).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Docente]:
        """Obtener todos los docentes con paginación"""
        return self.session.query(Docente).offset(skip).limit(limit).all()

    def update(self, docente_id: int, docente_data: dict) -> Optional[Docente]:
        """Actualizar un docente"""
        db_docente = self.get_by_id(docente_id)
        if db_docente:
            for key, value in docente_data.items():
                setattr(db_docente, key, value)
            self.session.commit()
            self.session.refresh(db_docente)
        return db_docente

    def delete(self, docente_id: int) -> bool:
        """Eliminar un docente"""
        db_docente = self.get_by_id(docente_id)
        if db_docente:
            self.session.delete(db_docente)
            self.session.commit()
            return True
        return False

    def search_by_nombre(self, nombre: str) -> List[Docente]:
        """Buscar docentes por nombre"""
        return self.session.query(Docente).filter(
            Docente.nombre.ilike(f"%{nombre}%")
        ).all()

    def get_active_docentes(self) -> List[Docente]:
        """Obtener solo docentes activos (si hubiera un campo activo)"""
        return self.session.query(Docente).all()  # Por ahora todos