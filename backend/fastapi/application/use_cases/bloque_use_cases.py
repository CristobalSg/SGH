from dataclasses import dataclass
from typing import Optional, List
from domain.ports import BloqueRepository
from domain.models import Bloque

@dataclass
class BloqueUseCases:
    repo: BloqueRepository

    def get_all(self) -> List[Bloque]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Bloque]:
        return self.repo.get_by_id(id)

    def create(self, dia_semana: int, hora_inicio: str, hora_fin: str) -> Bloque:
        bloque = Bloque(dia_semana=dia_semana, hora_inicio=hora_inicio, hora_fin=hora_fin)
        return self.repo.add(bloque)

    def update(self, id: int, dia_semana: int = None, 
              hora_inicio: str = None, hora_fin: str = None) -> Optional[Bloque]:
        bloque = self.repo.get_by_id(id)
        if bloque:
            if dia_semana:
                bloque.dia_semana = dia_semana
            if hora_inicio:
                bloque.hora_inicio = hora_inicio
            if hora_fin:
                bloque.hora_fin = hora_fin
            return self.repo.update(bloque)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
