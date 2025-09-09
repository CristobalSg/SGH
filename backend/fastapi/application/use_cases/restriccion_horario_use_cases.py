from dataclasses import dataclass
from typing import Optional, List
from domain.ports import RestriccionHorarioRepository
from domain.entities import RestriccionHorario, RestriccionHorarioCreate

@dataclass
class RestriccionHorarioUseCases:
    repo: RestriccionHorarioRepository

    def get_all(self) -> List[RestriccionHorario]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[RestriccionHorario]:
        return self.repo.get_by_id(id)

    def create(self, docente_id: int, dia_semana: int, hora_inicio: str,
              hora_fin: str, disponible: bool, descripcion: str = None) -> RestriccionHorario:
        restriccion_create = RestriccionHorarioCreate(
            docente_id=docente_id,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            disponible=disponible,
            descripcion=descripcion
        )
        return self.repo.create(restriccion_create)

    def update(self, id: int, dia_semana: int = None, hora_inicio: str = None,
              hora_fin: str = None, disponible: bool = None, descripcion: str = None) -> Optional[RestriccionHorario]:
        restriccion = self.repo.get_by_id(id)
        if restriccion:
            if dia_semana:
                restriccion.dia_semana = dia_semana
            if hora_inicio:
                restriccion.hora_inicio = hora_inicio
            if hora_fin:
                restriccion.hora_fin = hora_fin
            if disponible is not None:
                restriccion.disponible = disponible
            if descripcion:
                restriccion.descripcion = descripcion
            return self.repo.update(restriccion)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
