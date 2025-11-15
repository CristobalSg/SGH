"""
Servicio para generar archivos FET desde JSON
"""
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Optional
from datetime import datetime

from app.timetable_schemas import (
    TimetableGenerationRequest,
    TimetableGenerationResponse,
    TimeConstraint,
    BasicCompulsoryTimeConstraint,
    MinDaysBetweenActivitiesConstraint,
    TeacherNotAvailableConstraint,
    SpaceConstraint,
    BasicCompulsorySpaceConstraint,
)


class TimetableService:
    """Servicio para generación de archivos FET"""

    def __init__(self, output_dir: str = "/app/output"):
        """
        Inicializar servicio
        
        Args:
            output_dir: Directorio donde se guardarán los archivos FET
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_fet_file(
        self, request: TimetableGenerationRequest
    ) -> TimetableGenerationResponse:
        """
        Generar archivo FET desde el request JSON
        
        Args:
            request: Request con todos los datos del horario
            
        Returns:
            Response con el resultado de la generación
        """
        try:
            # Crear el XML del FET
            root = self._create_fet_xml(request)

            # Convertir a string con formato
            xml_string = self._prettify_xml(root)

            # Guardar el archivo
            file_path = self._save_fet_file(
                xml_string, request.metadata.timetable_id
            )

            return TimetableGenerationResponse(
                success=True,
                message="Archivo FET generado exitosamente",
                timetable_id=request.metadata.timetable_id,
                file_url=file_path,
                errors=[],
            )

        except Exception as e:
            return TimetableGenerationResponse(
                success=False,
                message=f"Error al generar archivo FET: {str(e)}",
                timetable_id=request.metadata.timetable_id,
                file_url=None,
                errors=[str(e)],
            )

    def _create_fet_xml(self, request: TimetableGenerationRequest) -> ET.Element:
        """
        Crear la estructura XML del archivo FET
        
        Args:
            request: Request con los datos
            
        Returns:
            Elemento raíz del XML
        """
        # Elemento raíz
        root = ET.Element("fet", version="6.5.5")

        # Metadata
        ET.SubElement(root, "Institution_Name").text = request.metadata.institution_name
        ET.SubElement(root, "Comments").text = (
            f"{request.metadata.comments}\n"
            f"Generado: {datetime.now().isoformat()}\n"
            f"ID: {request.metadata.timetable_id}\n"
            f"Semestre: {request.metadata.semester}"
        )

        # Days
        self._add_days(root, request)

        # Hours
        self._add_hours(root, request)

        # Subjects
        self._add_subjects(root, request)

        # Teachers
        self._add_teachers(root, request)

        # Students (Years and Groups)
        self._add_students(root, request)

        # Activities
        self._add_activities(root, request)

        # Buildings and Rooms
        self._add_buildings_and_rooms(root, request)

        # Time Constraints
        self._add_time_constraints(root, request)

        # Space Constraints
        self._add_space_constraints(root, request)

        return root

    def _add_days(self, root: ET.Element, request: TimetableGenerationRequest):
        """Agregar días de la semana"""
        days_list = ET.SubElement(root, "Days_List")
        ET.SubElement(days_list, "Number_of_Days").text = str(
            len(request.calendar.days)
        )

        for day in request.calendar.days:
            day_elem = ET.SubElement(days_list, "Day")
            ET.SubElement(day_elem, "Name").text = day.name
            ET.SubElement(day_elem, "Long_Name").text = day.long_name

    def _add_hours(self, root: ET.Element, request: TimetableGenerationRequest):
        """Agregar horas/bloques"""
        hours_list = ET.SubElement(root, "Hours_List")
        ET.SubElement(hours_list, "Number_of_Hours").text = str(
            len(request.calendar.hours)
        )

        for hour in request.calendar.hours:
            hour_elem = ET.SubElement(hours_list, "Hour")
            ET.SubElement(hour_elem, "Name").text = hour.name
            ET.SubElement(hour_elem, "Long_Name").text = hour.long_name

    def _add_subjects(self, root: ET.Element, request: TimetableGenerationRequest):
        """Agregar asignaturas"""
        subjects_list = ET.SubElement(root, "Subjects_List")

        for subject in request.subjects:
            subject_elem = ET.SubElement(subjects_list, "Subject")
            ET.SubElement(subject_elem, "Name").text = f"{subject.code} - {subject.name}"
            ET.SubElement(subject_elem, "Comments").text = subject.comments

    def _add_teachers(self, root: ET.Element, request: TimetableGenerationRequest):
        """Agregar docentes"""
        teachers_list = ET.SubElement(root, "Teachers_List")

        for teacher in request.teachers:
            teacher_elem = ET.SubElement(teachers_list, "Teacher")
            ET.SubElement(teacher_elem, "Name").text = teacher.name
            ET.SubElement(teacher_elem, "Target_Number_of_Hours").text = str(
                teacher.target_hours
            )
            ET.SubElement(teacher_elem, "Comments").text = teacher.comments

    def _add_students(self, root: ET.Element, request: TimetableGenerationRequest):
        """Agregar años y grupos de estudiantes"""
        students_list = ET.SubElement(root, "Students_List")

        for year in request.student_years:
            # Year
            year_elem = ET.SubElement(students_list, "Year")
            ET.SubElement(year_elem, "Name").text = year.name
            ET.SubElement(year_elem, "Number_of_Students").text = str(
                year.total_students
            )

            # Groups
            for group in year.groups:
                group_elem = ET.SubElement(students_list, "Group")
                ET.SubElement(group_elem, "Name").text = group.name
                ET.SubElement(group_elem, "Number_of_Students").text = str(
                    group.students
                )

                # Subgroups (opcional, por ahora vacío)
                subgroups = ET.SubElement(students_list, "Subgroup")
                ET.SubElement(subgroups, "Name").text = f"{group.name} subgroup"
                ET.SubElement(subgroups, "Number_of_Students").text = str(
                    group.students
                )

    def _add_activities(self, root: ET.Element, request: TimetableGenerationRequest):
        """Agregar actividades"""
        activities_list = ET.SubElement(root, "Activities_List")

        for activity in request.activities:
            if not activity.active:
                continue

            activity_elem = ET.SubElement(activities_list, "Activity")

            # Teacher
            ET.SubElement(activity_elem, "Teacher").text = next(
                (t.name for t in request.teachers if t.id == activity.teacher_id),
                "Unknown",
            )

            # Subject
            subject = next(
                (s for s in request.subjects if s.id == activity.subject_id), None
            )
            if subject:
                ET.SubElement(activity_elem, "Subject").text = (
                    f"{subject.code} - {subject.name}"
                )

            # Students
            if activity.students_reference.type == "year":
                year = next(
                    (
                        y
                        for y in request.student_years
                        if y.id == activity.students_reference.id
                    ),
                    None,
                )
                if year:
                    students_elem = ET.SubElement(activity_elem, "Students")
                    ET.SubElement(students_elem, "Year").text = year.name
            else:  # group
                for year in request.student_years:
                    group = next(
                        (
                            g
                            for g in year.groups
                            if g.id == activity.students_reference.id
                        ),
                        None,
                    )
                    if group:
                        students_elem = ET.SubElement(activity_elem, "Students")
                        ET.SubElement(students_elem, "Year").text = year.name
                        ET.SubElement(students_elem, "Group").text = group.name
                        break

            # Duration
            ET.SubElement(activity_elem, "Duration").text = str(activity.duration)
            ET.SubElement(activity_elem, "Total_Duration").text = str(
                activity.total_duration
            )

            # ID and Group ID
            ET.SubElement(activity_elem, "Id").text = str(activity.id)
            ET.SubElement(activity_elem, "Activity_Group_Id").text = str(
                activity.group_id
            )

            # Active
            ET.SubElement(activity_elem, "Active").text = (
                "true" if activity.active else "false"
            )

            # Comments
            ET.SubElement(activity_elem, "Comments").text = activity.comments

    def _add_buildings_and_rooms(
        self, root: ET.Element, request: TimetableGenerationRequest
    ):
        """Agregar edificios y salas"""
        # Buildings
        buildings_list = ET.SubElement(root, "Buildings_List")
        for building in request.space.buildings:
            building_elem = ET.SubElement(buildings_list, "Building")
            ET.SubElement(building_elem, "Name").text = building.name

        # Rooms
        rooms_list = ET.SubElement(root, "Rooms_List")
        for room in request.space.rooms:
            room_elem = ET.SubElement(rooms_list, "Room")
            ET.SubElement(room_elem, "Name").text = room.name
            
            # Building
            building = next(
                (b for b in request.space.buildings if b.id == room.building_id), None
            )
            if building:
                ET.SubElement(room_elem, "Building").text = building.name
            
            ET.SubElement(room_elem, "Capacity").text = str(room.capacity)
            ET.SubElement(room_elem, "Comments").text = room.comments

    def _add_time_constraints(
        self, root: ET.Element, request: TimetableGenerationRequest
    ):
        """Agregar restricciones de tiempo"""
        constraints_list = ET.SubElement(root, "Time_Constraints_List")

        for constraint in request.time_constraints:
            if not constraint.active:
                continue

            if isinstance(constraint, BasicCompulsoryTimeConstraint):
                self._add_basic_compulsory_time(constraints_list, constraint)

            elif isinstance(constraint, MinDaysBetweenActivitiesConstraint):
                self._add_min_days_between_activities(
                    constraints_list, constraint, request
                )

            elif isinstance(constraint, TeacherNotAvailableConstraint):
                self._add_teacher_not_available(
                    constraints_list, constraint, request
                )

    def _add_basic_compulsory_time(
        self, parent: ET.Element, constraint: BasicCompulsoryTimeConstraint
    ):
        """Restricción básica obligatoria"""
        elem = ET.SubElement(
            parent, "ConstraintBasicCompulsoryTime"
        )
        ET.SubElement(elem, "Weight_Percentage").text = str(int(constraint.weight))
        ET.SubElement(elem, "Active").text = "true" if constraint.active else "false"

    def _add_min_days_between_activities(
        self,
        parent: ET.Element,
        constraint: MinDaysBetweenActivitiesConstraint,
        request: TimetableGenerationRequest,
    ):
        """Mínimo días entre actividades"""
        elem = ET.SubElement(
            parent, "ConstraintMinDaysBetweenActivities"
        )
        ET.SubElement(elem, "Weight_Percentage").text = str(int(constraint.weight))
        ET.SubElement(elem, "Active").text = "true" if constraint.active else "false"
        ET.SubElement(elem, "Consecutive_If_Same_Day").text = "true"
        ET.SubElement(elem, "Number_of_Activities").text = str(
            len(constraint.activity_ids)
        )
        ET.SubElement(elem, "Activity_Id").text = " ".join(
            str(aid) for aid in constraint.activity_ids
        )
        ET.SubElement(elem, "MinDays").text = str(constraint.min_days)

    def _add_teacher_not_available(
        self,
        parent: ET.Element,
        constraint: TeacherNotAvailableConstraint,
        request: TimetableGenerationRequest,
    ):
        """Docente no disponible"""
        teacher = next(
            (t for t in request.teachers if t.id == constraint.teacher_id), None
        )
        if not teacher:
            return

        for slot in constraint.not_available_slots:
            elem = ET.SubElement(
                parent, "ConstraintTeacherNotAvailableTimes"
            )
            ET.SubElement(elem, "Weight_Percentage").text = str(
                int(constraint.weight)
            )
            ET.SubElement(elem, "Teacher").text = teacher.name
            ET.SubElement(elem, "Active").text = (
                "true" if constraint.active else "false"
            )

            # Day
            day = request.calendar.days[slot.day_index]
            ET.SubElement(elem, "Day").text = day.name

            # Hour
            hour = request.calendar.hours[slot.hour_index]
            ET.SubElement(elem, "Hour").text = hour.name

    def _add_space_constraints(
        self, root: ET.Element, request: TimetableGenerationRequest
    ):
        """Agregar restricciones de espacio"""
        constraints_list = ET.SubElement(root, "Space_Constraints_List")

        for constraint in request.space.space_constraints:
            if not constraint.active:
                continue

            if isinstance(constraint, BasicCompulsorySpaceConstraint):
                elem = ET.SubElement(
                    constraints_list, "ConstraintBasicCompulsorySpace"
                )
                ET.SubElement(elem, "Weight_Percentage").text = str(
                    int(constraint.weight)
                )
                ET.SubElement(elem, "Active").text = (
                    "true" if constraint.active else "false"
                )

    def _prettify_xml(self, elem: ET.Element) -> str:
        """
        Formatear XML con indentación
        
        Args:
            elem: Elemento raíz
            
        Returns:
            String XML formateado
        """
        rough_string = ET.tostring(elem, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    def _save_fet_file(self, xml_content: str, timetable_id: str) -> str:
        """
        Guardar el archivo FET
        
        Args:
            xml_content: Contenido XML
            timetable_id: ID del horario
            
        Returns:
            Path del archivo guardado
        """
        filename = f"timetable_{timetable_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.fet"
        file_path = os.path.join(self.output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        return file_path


# Instancia singleton del servicio
timetable_service = TimetableService()
