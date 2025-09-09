from dataclasses import dataclass
from typing import Optional, List
from domain.ports import RestriccionRepositoryPort
from domain.entities import RestriccionCreate, Restriccion

@dataclass
class RestriccionUseCases:
    repo: RestriccionRepositoryPort

    def get_all(self) -> List[Restriccion]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Restriccion]:
        return self.repo.get_by_id(id)

    def create(self, docente_id: int, tipo: str, valor: str, prioridad: int,
              restriccion_blanda: str, restriccion_dura: str) -> Restriccion:
        restriccion_data = RestriccionCreate(
            docente_id=docente_id,
            tipo=tipo,
            valor=valor,
            prioridad=prioridad,
            restriccion_blanda=restriccion_blanda,
            restriccion_dura=restriccion_dura
        )
        return self.repo.create(restriccion_data)

    def update(self, id: int, tipo: str = None, valor: str = None,
              prioridad: int = None, restriccion_blanda: str = None,
              restriccion_dura: str = None) -> Optional[Restriccion]:
        update_data = {}
        if tipo is not None:
            update_data["tipo"] = tipo
        if valor is not None:
            update_data["valor"] = valor
        if prioridad is not None:
            update_data["prioridad"] = prioridad
        if restriccion_blanda is not None:
            update_data["restriccion_blanda"] = restriccion_blanda
        if restriccion_dura is not None:
            update_data["restriccion_dura"] = restriccion_dura
        
        if update_data:
            return self.repo.update(id, update_data)
        return self.repo.get_by_id(id)

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
