from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models import Docente, Restriccion, Bloque, RestriccionHorario
from domain.entities import (
    DocenteCreate, RestriccionCreate, BloqueCreate,
    RestriccionHorarioCreate
)

class SQLDocenteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, docente: DocenteCreate) -> Docente:
        db_docente = Docente(**docente.dict())
        self.session.add(db_docente)
        self.session.commit()
        self.session.refresh(db_docente)
        return db_docente

    def get_by_id(self, docente_id: int) -> Optional[Docente]:
        return self.session.query(Docente).filter(Docente.id == docente_id).first()

    def get_by_email(self, email: str) -> Optional[Docente]:
        return self.session.query(Docente).filter(Docente.email == email).first()

    def get_all(self) -> List[Docente]:
        return self.session.query(Docente).all()

    def update(self, docente_id: int, docente_data: dict) -> Optional[Docente]:
        db_docente = self.get_by_id(docente_id)
        if db_docente:
            for key, value in docente_data.items():
                setattr(db_docente, key, value)
            self.session.commit()
            self.session.refresh(db_docente)
        return db_docente

    def delete(self, docente_id: int) -> bool:
        db_docente = self.get_by_id(docente_id)
        if db_docente:
            self.session.delete(db_docente)
            self.session.commit()
            return True
        return False

class SQLRestriccionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, restriccion: RestriccionCreate) -> Restriccion:
        db_restriccion = Restriccion(**restriccion.dict())
        self.session.add(db_restriccion)
        self.session.commit()
        self.session.refresh(db_restriccion)
        return db_restriccion

    def get_by_id(self, restriccion_id: int) -> Optional[Restriccion]:
        return self.session.query(Restriccion).filter(Restriccion.id == restriccion_id).first()

    def get_all(self) -> List[Restriccion]:
        return self.session.query(Restriccion).all()

    def get_by_docente(self, docente_id: int) -> List[Restriccion]:
        return self.session.query(Restriccion).filter(Restriccion.docente_id == docente_id).all()

    def update(self, restriccion_id: int, restriccion_data: dict) -> Optional[Restriccion]:
        db_restriccion = self.get_by_id(restriccion_id)
        if db_restriccion:
            for key, value in restriccion_data.items():
                setattr(db_restriccion, key, value)
            self.session.commit()
            self.session.refresh(db_restriccion)
        return db_restriccion

    def delete(self, restriccion_id: int) -> bool:
        db_restriccion = self.get_by_id(restriccion_id)
        if db_restriccion:
            self.session.delete(db_restriccion)
            self.session.commit()
            return True
        return False

class SQLBloqueRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, bloque: BloqueCreate) -> Bloque:
        db_bloque = Bloque(**bloque.dict())
        self.session.add(db_bloque)
        self.session.commit()
        self.session.refresh(db_bloque)
        return db_bloque

    def get_by_id(self, bloque_id: int) -> Optional[Bloque]:
        return self.session.query(Bloque).filter(Bloque.id == bloque_id).first()

    def get_all(self) -> List[Bloque]:
        return self.session.query(Bloque).all()

    def update(self, bloque_id: int, bloque_data: dict) -> Optional[Bloque]:
        db_bloque = self.get_by_id(bloque_id)
        if db_bloque:
            for key, value in bloque_data.items():
                setattr(db_bloque, key, value)
            self.session.commit()
            self.session.refresh(db_bloque)
        return db_bloque

    def delete(self, bloque_id: int) -> bool:
        db_bloque = self.get_by_id(bloque_id)
        if db_bloque:
            self.session.delete(db_bloque)
            self.session.commit()
            return True
        return False

class SQLRestriccionHorarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, restriccion: RestriccionHorarioCreate) -> RestriccionHorario:
        db_restriccion = RestriccionHorario(**restriccion.dict())
        self.session.add(db_restriccion)
        self.session.commit()
        self.session.refresh(db_restriccion)
        return db_restriccion

    def get_by_id(self, restriccion_id: int) -> Optional[RestriccionHorario]:
        return self.session.query(RestriccionHorario).filter(RestriccionHorario.id == restriccion_id).first()

    def get_by_docente(self, docente_id: int) -> List[RestriccionHorario]:
        return self.session.query(RestriccionHorario).filter(RestriccionHorario.docente_id == docente_id).all()

    def update(self, restriccion_id: int, restriccion_data: dict) -> Optional[RestriccionHorario]:
        db_restriccion = self.get_by_id(restriccion_id)
        if db_restriccion:
            for key, value in restriccion_data.items():
                setattr(db_restriccion, key, value)
            self.session.commit()
            self.session.refresh(db_restriccion)
        return db_restriccion

    def delete(self, restriccion_id: int) -> bool:
        db_restriccion = self.get_by_id(restriccion_id)
        if db_restriccion:
            self.session.delete(db_restriccion)
            self.session.commit()
            return True
        return False
