"""
Servicio para generar horarios con FET
"""
from typing import List
import httpx
from fastapi import HTTPException, status

from domain.timetable_schemas import (
    TimetableGenerationRequest,
    TimetableGenerationResponse,
    TimetableMetadata,
    Calendar,
    CalendarDay,
    CalendarHour,
    Subject,
    Teacher,
    StudentYear,
    StudentGroup,
    Activity,
    StudentsReference,
    TimeConstraint,
    TeacherNotAvailableConstraint,
    NotAvailableSlot,
    BasicCompulsoryTimeConstraint,
    Space,
    Building,
    Room,
    BasicCompulsorySpaceConstraint,
)
from infrastructure.repositories.docente_repository import DocenteRepository
from infrastructure.repositories.asignatura_repository import AsignaturaRepository
from infrastructure.repositories.seccion_repository import SeccionRepository
from infrastructure.repositories.clase_repository import ClaseRepository
from infrastructure.repositories.sala_repository import SalaRepository
from infrastructure.repositories.edificio_repository import SQLEdificioRepository
from infrastructure.repositories.user_repository import SQLUserRepository
from config import settings


class TimetableService:
    """Servicio para generar horarios"""

    def __init__(
        self,
        docente_repository: DocenteRepository,
        asignatura_repository: AsignaturaRepository,
        seccion_repository: SeccionRepository,
        clase_repository: ClaseRepository,
        sala_repository: SalaRepository,
        edificio_repository: SQLEdificioRepository,
        user_repository: SQLUserRepository,
    ):
        self.docente_repository = docente_repository
        self.asignatura_repository = asignatura_repository
        self.seccion_repository = seccion_repository
        self.clase_repository = clase_repository
        self.sala_repository = sala_repository
        self.edificio_repository = edificio_repository
        self.user_repository = user_repository
        self.agent_url = settings.agent_api_url or "http://agent:8200"

    def _get_static_calendar(self) -> Calendar:
        """Obtener calendario estático (5 días, 10 bloques)"""
        days = [
            CalendarDay(index=0, name="lunes", long_name="Lunes"),
            CalendarDay(index=1, name="martes", long_name="Martes"),
            CalendarDay(index=2, name="miercoles", long_name="Miércoles"),
            CalendarDay(index=3, name="jueves", long_name="Jueves"),
            CalendarDay(index=4, name="viernes", long_name="Viernes"),
        ]

        hours = [
            CalendarHour(index=0, name="08:00 - 09:00", long_name="Bloque 1"),
            CalendarHour(index=1, name="09:10 - 10:10", long_name="Bloque 2"),
            CalendarHour(index=2, name="10:20 - 11:20", long_name="Bloque 3"),
            CalendarHour(index=3, name="11:30 - 12:30", long_name="Bloque 4"),
            CalendarHour(index=4, name="12:40 - 13:40", long_name="Bloque 5"),
            CalendarHour(index=5, name="13:50 - 14:50", long_name="Bloque 6"),
            CalendarHour(index=6, name="15:00 - 16:00", long_name="Bloque 7"),
            CalendarHour(index=7, name="16:10 - 17:10", long_name="Bloque 8"),
            CalendarHour(index=8, name="17:20 - 18:20", long_name="Bloque 9"),
            CalendarHour(index=9, name="18:30 - 19:30", long_name="Bloque 10"),
        ]

        return Calendar(days=days, hours=hours)

    def _get_static_student_years(self) -> List[StudentYear]:
        """Obtener años y grupos desde la base de datos"""
        from collections import defaultdict
        
        # Obtener todas las secciones
        secciones_db = self.seccion_repository.get_all()
        
        # Agrupar por año académico
        años_dict = defaultdict(lambda: {"grupos": [], "total": 0})
        
        for seccion in secciones_db:
            año = seccion.anio_academico
            
            # Generar ID del grupo según tipo
            if seccion.tipo_grupo == "seccion":
                group_id = f"g-{año}-seccion-{seccion.id}"
            elif seccion.tipo_grupo == "mencion":
                group_id = f"g-{año}-mencion-{seccion.id}"
            elif seccion.tipo_grupo == "base":
                group_id = f"g-{año}-seccion-{seccion.id}"
            else:
                group_id = f"g-{año}-grupo-{seccion.id}"
            
            # Agregar grupo
            años_dict[año]["grupos"].append(
                StudentGroup(
                    id=group_id,
                    name=seccion.codigo,  # "1 sección 1", "5 mención 1", etc.
                    students=seccion.numero_estudiantes
                )
            )
            años_dict[año]["total"] += seccion.numero_estudiantes
        
        # Construir lista de StudentYear
        student_years = []
        for año in sorted(años_dict.keys()):
            student_years.append(
                StudentYear(
                    id=f"year-{año}",
                    name=str(año),
                    total_students=años_dict[año]["total"],
                    groups=años_dict[año]["grupos"]
                )
            )
        
        return student_years

    def _build_subjects(self) -> List[Subject]:
        """Construir lista de asignaturas desde la BD"""
        asignaturas_db = self.asignatura_repository.get_all()
        return [
            Subject(
                id=f"sub-{asig.id}",
                name=asig.nombre,
                code=asig.codigo,
                comments="",
            )
            for asig in asignaturas_db
        ]

    def _build_teachers(self) -> List[Teacher]:
        """Construir lista de docentes desde la BD"""
        docentes_db = self.docente_repository.get_all()
        teachers = []

        for docente in docentes_db:
            # Obtener el usuario asociado
            user = self.user_repository.get_by_id(docente.user_id)
            if user:
                teachers.append(
                    Teacher(
                        id=f"t-{docente.user_id}",
                        name=user.nombre,
                        target_hours=0,
                        comments=f"Departamento: {docente.departamento}",
                    )
                )

        return teachers

    def _build_activities(self) -> List[Activity]:
        """Construir actividades desde las clases programadas"""
        clases_db = self.clase_repository.get_all()
        activities = []
        
        # Agrupar clases por sección para calcular duración total
        from collections import defaultdict
        clases_por_seccion = defaultdict(list)
        
        for clase in clases_db:
            if clase.seccion_id:
                clases_por_seccion[clase.seccion_id].append(clase)
        
        activity_id = 1
        for seccion_id, clases in clases_por_seccion.items():
            # Obtener información de la primera clase
            primera_clase = clases[0]
            
            # Obtener seccion
            seccion = self.seccion_repository.get_by_id(seccion_id)
            if not seccion:
                continue
                
            # Obtener la asignatura
            asignatura = self.asignatura_repository.get_by_id(seccion.asignatura_id)
            if not asignatura:
                continue

            # Determinar referencia al grupo específico de la sección
            if seccion.tipo_grupo == "seccion":
                group_id = f"g-{seccion.anio_academico}-seccion-{seccion.id}"
            elif seccion.tipo_grupo == "mencion":
                group_id = f"g-{seccion.anio_academico}-mencion-{seccion.id}"
            elif seccion.tipo_grupo == "base":
                group_id = f"g-{seccion.anio_academico}-seccion-{seccion.id}"
            else:
                group_id = f"g-{seccion.anio_academico}-grupo-{seccion.id}"
            
            students_ref = StudentsReference(type="group", id=group_id)

            # Calcular duración basada en horas de la asignatura
            # Usar horas_presenciales como base (convertir a bloques de 1 hora)
            total_duration = asignatura.horas_presenciales + asignatura.horas_mixtas
            duration = min(2, total_duration)  # 2 bloques consecutivos por defecto, ajustable
            
            # Crear actividad
            activities.append(
                Activity(
                    id=str(activity_id),
                    group_id=str(seccion.id * 100),  # group_id como string
                    teacher_id=f"t-{primera_clase.docente_id}",
                    subject_id=f"sub-{asignatura.id}",
                    students_reference=students_ref,
                    duration=duration,
                    total_duration=total_duration,
                    active=True,
                    comments=f"Sección: {seccion.codigo}",
                )
            )
            activity_id += 1

        return activities

    def _build_time_constraints(self) -> List[TimeConstraint]:
        """Devolver restricciones de tiempo vacías (no se usan de momento)"""
        return []

    def _build_space(self) -> Space:
        """Construir configuración de espacios"""
        # Obtener edificios
        edificios_db = self.edificio_repository.get_all()
        buildings = [
            Building(id=f"b-{edif.id}", name=edif.nombre, comments="") for edif in edificios_db
        ]

        # Obtener salas
        salas_db = self.sala_repository.get_all()
        rooms = [
            Room(
                id=f"r-{sala.id}",
                name=sala.numero,
                building_id=f"b-{sala.edificio_id}",
                capacity=sala.capacidad,
                comments="",
            )
            for sala in salas_db
        ]

        # Restricción básica de espacio
        space_constraints = [
            BasicCompulsorySpaceConstraint(
                type="basic_compulsory_space", weight=100.0, active=True
            )
        ]

        return Space(
            buildings=buildings, rooms=rooms, space_constraints=space_constraints
        )

    async def generate_timetable(
        self, semester: str, institution_name: str
    ) -> TimetableGenerationResponse:
        """
        Generar horario completo y enviarlo al agente
        """
        try:
            # Construir metadata
            timetable_id = f"{semester}-{institution_name.lower().replace(' ', '-')}"
            metadata = TimetableMetadata(
                timetable_id=timetable_id,
                semester=semester,
                institution_name=institution_name,
                comments="Generado desde SGH",
            )

            # Construir request completo
            request = TimetableGenerationRequest(
                metadata=metadata,
                calendar=self._get_static_calendar(),
                subjects=self._build_subjects(),
                teachers=self._build_teachers(),
                student_years=self._get_static_student_years(),
                activities=self._build_activities(),
                time_constraints=self._build_time_constraints(),
                space=self._build_space(),
            )

            # Enviar al agente
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self.agent_url}/timetable/generate",
                    json=request.model_dump(),
                    headers={
                        "Authorization": f"Bearer {settings.service_auth_token}",
                        "X-Service-Name": "sgh-backend",
                    },
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Error del agente: {response.text}",
                    )

                result = response.json()
                return TimetableGenerationResponse(**result)

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"No se pudo conectar con el agente: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar horario: {str(e)}",
            )
