from dataclasses import dataclass
from typing import Optional, List
from domain.ports import DocenteRepository
from domain.models import Docente

@dataclass
class DocenteUseCases:
    repo: DocenteRepository

    def get_all(self) -> List[Docente]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Docente]:
        return self.repo.get_by_id(id)

    def create(self, nombre: str, email: str, pass_hash: str) -> Docente:
        docente = Docente(nombre=nombre, email=email, pass_hash=pass_hash)
        return self.repo.add(docente)

    def update(self, id: int, nombre: str = None, email: str = None, pass_hash: str = None) -> Optional[Docente]:
        docente = self.repo.get_by_id(id)
        if docente:
            if nombre:
                docente.nombre = nombre
            if email:
                docente.email = email
            if pass_hash:
                docente.pass_hash = pass_hash
            return self.repo.update(docente)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
