from dataclasses import dataclass
from typing import Optional, List
from domain.ports import AsignaturaRepository
from domain.models import Asignatura

@dataclass
class AsignaturaUseCases:
    repo: AsignaturaRepository

    def get_all(self) -> List[Asignatura]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Asignatura]:
        return self.repo.get_by_id(id)

    def create(self, codigo: str, nombre: str, creditos: int) -> Asignatura:
        asignatura = Asignatura(codigo=codigo, nombre=nombre, creditos=creditos)
        return self.repo.add(asignatura)

    def update(self, id: int, codigo: str = None, nombre: str = None, creditos: int = None) -> Optional[Asignatura]:
        asignatura = self.repo.get_by_id(id)
        if asignatura:
            if codigo:
                asignatura.codigo = codigo
            if nombre:
                asignatura.nombre = nombre
            if creditos:
                asignatura.creditos = creditos
            return self.repo.update(asignatura)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)