from dataclasses import dataclass
from typing import Optional, List
from domain.ports import RestriccionRepository
from domain.models import Restriccion

@dataclass
class RestriccionUseCases:
    repo: RestriccionRepository

    def get_all(self) -> List[Restriccion]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Restriccion]:
        return self.repo.get_by_id(id)

    def create(self, docente_id: int, tipo: str, valor: str, prioridad: int,
              restriccion_blanda: str, restriccion_dura: str) -> Restriccion:
        restriccion = Restriccion(
            docente_id=docente_id,
            tipo=tipo,
            valor=valor,
            prioridad=prioridad,
            restriccion_blanda=restriccion_blanda,
            restriccion_dura=restriccion_dura
        )
        return self.repo.add(restriccion)

    def update(self, id: int, tipo: str = None, valor: str = None,
              prioridad: int = None, restriccion_blanda: str = None,
              restriccion_dura: str = None) -> Optional[Restriccion]:
        restriccion = self.repo.get_by_id(id)
        if restriccion:
            if tipo:
                restriccion.tipo = tipo
            if valor:
                restriccion.valor = valor
            if prioridad:
                restriccion.prioridad = prioridad
            if restriccion_blanda:
                restriccion.restriccion_blanda = restriccion_blanda
            if restriccion_dura:
                restriccion.restriccion_dura = restriccion_dura
            return self.repo.update(restriccion)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
