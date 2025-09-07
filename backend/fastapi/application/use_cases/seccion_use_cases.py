from dataclasses import dataclass
from typing import Optional, List
from domain.ports import SeccionRepository
from domain.models import Seccion

@dataclass
class SeccionUseCases:
    repo: SeccionRepository

    def get_all(self) -> List[Seccion]:
        return self.repo.get_all()

    def get_by_id(self, id: int) -> Optional[Seccion]:
        return self.repo.get_by_id(id)

    def create(self, codigo: str, anio: int, semestre: int, asignatura_id: int, cupos: int) -> Seccion:
        seccion = Seccion(
            codigo=codigo,
            anio=anio,
            semestre=semestre,
            asignatura_id=asignatura_id,
            cupos=cupos
        )
        return self.repo.add(seccion)

    def update(self, id: int, codigo: str = None, anio: int = None,
              semestre: int = None, cupos: int = None) -> Optional[Seccion]:
        seccion = self.repo.get_by_id(id)
        if seccion:
            if codigo:
                seccion.codigo = codigo
            if anio:
                seccion.anio = anio
            if semestre:
                seccion.semestre = semestre
            if cupos:
                seccion.cupos = cupos
            return self.repo.update(seccion)
        return None

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
