from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import RestriccionHorario, RestriccionHorarioCreate
from infrastructure.repositories.restriccion_horario_repository import RestriccionHorarioRepository

class RestriccionHorarioUseCases:
    def __init__(self, restriccion_horario_repository: RestriccionHorarioRepository):
        self.restriccion_horario_repository = restriccion_horario_repository

    def get_all(self, skip: int = 0, limit: int = 100) -> List[RestriccionHorario]:
        """Obtener todas las restricciones de horario con paginación"""
        return self.restriccion_horario_repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, restriccion_id: int) -> RestriccionHorario:
        """Obtener restricción de horario por ID"""
        restriccion = self.restriccion_horario_repository.get_by_id(restriccion_id)
        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción de horario no encontrada"
            )
        return restriccion

    def create(self, restriccion_data: RestriccionHorarioCreate) -> RestriccionHorario:
        """Crear una nueva restricción de horario"""
        # Verificar si ya existe una restricción similar para el mismo docente y horario
        restricciones_existentes = self.restriccion_horario_repository.get_by_docente_y_horario(
            restriccion_data.docente_id,
            restriccion_data.dia_semana,
            restriccion_data.hora_inicio,
            restriccion_data.hora_fin
        )
        
        if restricciones_existentes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una restricción de horario para el docente en ese período"
            )
        
        return self.restriccion_horario_repository.create(restriccion_data)

    def update(self, restriccion_id: int, **update_data) -> RestriccionHorario:
        """Actualizar una restricción de horario"""
        # Verificar que la restricción existe
        existing_restriccion = self.restriccion_horario_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción de horario no encontrada"
            )
        
        updated_restriccion = self.restriccion_horario_repository.update(restriccion_id, update_data)
        if not updated_restriccion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la restricción de horario"
            )
        return updated_restriccion

    def delete(self, restriccion_id: int) -> bool:
        """Eliminar una restricción de horario"""
        # Verificar que la restricción existe
        existing_restriccion = self.restriccion_horario_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción de horario no encontrada"
            )
        
        success = self.restriccion_horario_repository.delete(restriccion_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la restricción de horario"
            )
        return success

    def get_by_docente(self, docente_id: int) -> List[RestriccionHorario]:
        """Obtener restricciones de horario de un docente específico"""
        return self.restriccion_horario_repository.get_by_docente(docente_id)

    def get_by_dia_semana(self, dia_semana: int) -> List[RestriccionHorario]:
        """Obtener restricciones de horario por día de la semana"""
        return self.restriccion_horario_repository.get_by_dia_semana(dia_semana)

    def get_disponibilidad_docente(self, docente_id: int, dia_semana: int = None) -> List[RestriccionHorario]:
        """Obtener disponibilidad de un docente (solo restricciones marcadas como disponibles)"""
        return self.restriccion_horario_repository.get_disponibilidad_docente(docente_id, dia_semana)

    def delete_by_docente(self, docente_id: int) -> int:
        """Eliminar todas las restricciones de horario de un docente"""
        return self.restriccion_horario_repository.delete_by_docente(docente_id)
