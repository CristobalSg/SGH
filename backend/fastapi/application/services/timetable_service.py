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
from infrastructure.repositories.restriccion_horario_repository import (
    RestriccionHorarioRepository,
)
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
        restriccion_horario_repository: RestriccionHorarioRepository,
        sala_repository: SalaRepository,
        edificio_repository: SQLEdificioRepository,
        user_repository: SQLUserRepository,
    ):
        self.docente_repository = docente_repository
        self.asignatura_repository = asignatura_repository
        self.seccion_repository = seccion_repository
        self.restriccion_horario_repository = restriccion_horario_repository
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
        """Obtener años y grupos estáticos"""
        return [
            StudentYear(
                id="year-1",
                name="1",
                total_students=90,
                groups=[
                    StudentGroup(id="g-1-seccion-1", name="1 sección 1", students=30),
                    StudentGroup(id="g-1-seccion-2", name="1 sección 2", students=30),
                    StudentGroup(id="g-1-seccion-3", name="1 sección 3", students=30),
                ],
            ),
            StudentYear(
                id="year-2",
                name="2",
                total_students=80,
                groups=[
                    StudentGroup(id="g-2-seccion-1", name="2 sección 1", students=40),
                    StudentGroup(id="g-2-seccion-2", name="2 sección 2", students=40),
                ],
            ),
            StudentYear(
                id="year-3",
                name="3",
                total_students=70,
                groups=[
                    StudentGroup(id="g-3-seccion-1", name="3 sección 1", students=35),
                    StudentGroup(id="g-3-seccion-2", name="3 sección 2", students=35),
                ],
            ),
            StudentYear(
                id="year-4",
                name="4",
                total_students=60,
                groups=[
                    StudentGroup(id="g-4-seccion-1", name="4 sección 1", students=30),
                    StudentGroup(id="g-4-seccion-2", name="4 sección 2", students=30),
                ],
            ),
        ]

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
        """Construir actividades desde las secciones"""
        secciones_db = self.seccion_repository.get_all()
        activities = []
        activity_id = 1

        for seccion in secciones_db:
            # Buscar la asignatura
            asignatura = self.asignatura_repository.get_by_id(seccion.asignatura_id)
            if not asignatura:
                continue

            # Buscar el docente
            docente = self.docente_repository.get_by_id(seccion.docente_id)
            if not docente:
                continue

            # Determinar grupo de estudiantes (usar año académico por defecto)
            # En producción, esto vendría de la relación seccion-estudiantes
            students_ref = StudentsReference(type="year", id=f"year-{seccion.anio}")

            # Crear actividad
            # duration y total_duration deberían venir de la configuración de la asignatura
            activities.append(
                Activity(
                    id=str(activity_id),
                    group_id=str(seccion.id * 100),  # group_id como string
                    teacher_id=f"t-{docente.user_id}",
                    subject_id=f"sub-{asignatura.id}",
                    students_reference=students_ref,
                    duration=2,  # 2 bloques consecutivos por defecto
                    total_duration=4,  # 4 bloques totales por semana
                    active=True,
                    comments=f"Sección: {seccion.codigo}",
                )
            )
            activity_id += 1

        return activities

    def _build_time_constraints(self) -> List[TimeConstraint]:
        """Construir restricciones de tiempo"""
        constraints = []

        # Restricción básica obligatoria
        constraints.append(
            BasicCompulsoryTimeConstraint(
                type="basic_compulsory_time", weight=100.0, active=True
            )
        )

        # Restricciones de disponibilidad de docentes
        docentes_db = self.docente_repository.get_all()
        for docente in docentes_db:
            restricciones = self.restriccion_horario_repository.get_by_docente(docente.id)

            not_available_slots = []
            for restriccion in restricciones:
                # Solo restricciones de NO disponibilidad
                if not restriccion.disponible and restriccion.activa:
                    # Convertir día de semana y bloques a slots
                    # Aquí necesitarías convertir hora_inicio/hora_fin a índices de bloque
                    # Por simplicidad, usar el día directamente
                    not_available_slots.append(
                        NotAvailableSlot(
                            day_index=restriccion.dia_semana,
                            hour_index=0,  # Necesitarías calcular esto desde hora_inicio
                        )
                    )

            if not_available_slots:
                constraints.append(
                    TeacherNotAvailableConstraint(
                        type="teacher_not_available",
                        weight=100.0,
                        active=True,
                        teacher_id=f"t-{docente.user_id}",
                        not_available_slots=not_available_slots,
                    )
                )

        return constraints

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
