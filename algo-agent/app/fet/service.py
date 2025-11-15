import subprocess
from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import models
from app.settings import AppSettings


class FetData(BaseModel):
    docentes: List[dict] = Field(default_factory=list)
    asignaturas: List[dict] = Field(default_factory=list)
    secciones: List[dict] = Field(default_factory=list)
    salas: List[dict] = Field(default_factory=list)
    bloques: List[dict] = Field(default_factory=list)
    restricciones: List[dict] = Field(default_factory=list)


class FetRunResult(BaseModel):
    input_file: str
    output_directory: str
    stdout: str = ""
    stderr: str = ""
    return_code: int


class FetService:
    def __init__(self, db: Session, settings: AppSettings):
        self.db = db
        self.settings = settings

    def run(self) -> FetRunResult:
        dataset = self.collect_data()
        input_file = self.build_input_file(dataset)
        return self.execute_algorithm(input_file)

    def collect_data(self) -> FetData:
        docentes = [
            {
                "id": docente.id,
                "user_id": docente.user_id,
                "nombre": docente.user.nombre if docente.user else None,
                "departamento": docente.departamento,
            }
            for docente in self.db.query(models.Docente).all()
        ]

        asignaturas = [
            {
                "id": asignatura.id,
                "codigo": asignatura.codigo,
                "nombre": asignatura.nombre,
                "creditos": asignatura.creditos,
            }
            for asignatura in self.db.query(models.Asignatura).all()
        ]

        secciones = [
            {
                "id": seccion.id,
                "codigo": seccion.codigo,
                "anio": seccion.anio,
                "semestre": seccion.semestre,
                "asignatura_id": seccion.asignatura_id,
                "cupos": seccion.cupos,
            }
            for seccion in self.db.query(models.Seccion).all()
        ]

        salas = [
            {
                "id": sala.id,
                "codigo": sala.codigo,
                "capacidad": sala.capacidad,
                "tipo": sala.tipo,
                "disponible": sala.disponible,
                "equipamiento": sala.equipamiento,
                "edificio_id": sala.edificio_id,
            }
            for sala in self.db.query(models.Sala).all()
        ]

        bloques = [
            {
                "id": bloque.id,
                "dia_semana": bloque.dia_semana,
                "hora_inicio": bloque.hora_inicio.isoformat() if bloque.hora_inicio else None,
                "hora_fin": bloque.hora_fin.isoformat() if bloque.hora_fin else None,
            }
            for bloque in self.db.query(models.Bloque).all()
        ]

        restricciones = [
            {
                "id": restriccion.id,
                "docente_id": restriccion.docente_id,
                "tipo": restriccion.tipo,
                "valor": restriccion.valor,
                "prioridad": restriccion.prioridad,
                "blanda": restriccion.restriccion_blanda,
                "dura": restriccion.restriccion_dura,
            }
            for restriccion in self.db.query(models.Restriccion).all()
        ]

        return FetData(
            docentes=docentes,
            asignaturas=asignaturas,
            secciones=secciones,
            salas=salas,
            bloques=bloques,
            restricciones=restricciones,
        )

    def build_input_file(self, dataset: FetData) -> Path:
        workdir = self.settings.fet_workdir
        workdir.mkdir(parents=True, exist_ok=True)
        file_path = workdir / f"fet-input-{uuid4().hex}.json"
        file_path.write_text(dataset.model_dump_json(indent=2), encoding="utf-8")
        return file_path

    def execute_algorithm(self, input_file: Path) -> FetRunResult:
        binary = self.settings.fet_binary_path
        if not binary.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"No se encontró el binario de FET en {binary}",
            )

        try:
            completed = subprocess.run(
                [str(binary), str(input_file)],
                capture_output=True,
                text=True,
                cwd=binary.parent,
                timeout=self.settings.fet_timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:  # noqa: F841
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="La ejecución de FET superó el tiempo máximo permitido",
            ) from None
        except FileNotFoundError as exc:  # noqa: F841
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo ejecutar el binario de FET",
            ) from None

        if completed.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="FET finalizó con errores",
            )

        return FetRunResult(
            input_file=str(input_file),
            output_directory=str(self.settings.fet_workdir),
            stdout=completed.stdout,
            stderr=completed.stderr,
            return_code=completed.returncode,
        )


__all__ = ["FetService", "FetData", "FetRunResult"]
