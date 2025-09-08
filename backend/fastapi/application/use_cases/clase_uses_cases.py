from dataclasses import dataclass
from typing import Optional, List
from domain.ports import ClaseRepository
from domain.models import Clase

@dataclass
class ClaseUseCases:
    repo: ClaseRepository

    def get_all(self) -> List[Clase]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Clase]:
        return self.repo.get_by_id(id)

    def create(self, seccion_id: int, docente_id: int, sala_id: int, 
              bloque_id: int, estado: str) -> Clase:
        clase = Clase(
            seccion_id=seccion_id,
            docente_id=docente_id,
            sala_id=sala_id,
            bloque_id=bloque_id,
            estado=estado
        )
        return self.repo.add(clase)

    def update(self, id: int, seccion_id: int = None, docente_id: int = None,
              sala_id: int = None, bloque_id: int = None, estado: str = None) -> Optional[Clase]:
        clase = self.repo.get_by_id(id)
        if clase:
            if seccion_id:
                clase.seccion_id = seccion_id
            if docente_id:
                clase.docente_id = docente_id
            if sala_id:
                clase.sala_id = sala_id
            if bloque_id:
                clase.bloque_id = bloque_id
            if estado:
                clase.estado = estado
            return self.repo.update(clase)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
