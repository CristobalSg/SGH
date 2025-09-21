from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models import Docente
from domain.entities import DocenteCreate

class DocenteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, docente: DocenteCreate) -> Docente:
        """Crear un nuevo docente"""
        db_docente = Docente(**docente.model_dump())
        self.session.add(db_docente)
        self.session.commit()
        self.session.refresh(db_docente)
        return db_docente

    def get_by_id(self, docente_id: int) -> Optional[Docente]:
        """Obtener docente por ID"""
        return self.session.query(Docente).filter(Docente.id == docente_id).first()

    def get_by_email(self, email: str) -> Optional[Docente]:
        """Obtener docente por email"""
        return self.session.query(Docente).filter(Docente.email == email).first()

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