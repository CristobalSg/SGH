from dataclasses import dataclass
from typing import Optional, List
from domain.ports import SalaRepository
from domain.models import Sala

@dataclass
class SalaUseCases:
    repo: SalaRepository

    def get_all(self) -> List[Sala]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Sala]:
        return self.repo.get_by_id(id)

    def create(self, codigo: str, capacidad: int, tipo: str) -> Sala:
        sala = Sala(codigo=codigo, capacidad=capacidad, tipo=tipo)
        return self.repo.add(sala)

    def update(self, id: int, codigo: str = None, capacidad: int = None, tipo: str = None) -> Optional[Sala]:
        sala = self.repo.get_by_id(id)
        if sala:
            if codigo:
                sala.codigo = codigo
            if capacidad:
                sala.capacidad = capacidad
            if tipo:
                sala.tipo = tipo
            return self.repo.update(sala)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
