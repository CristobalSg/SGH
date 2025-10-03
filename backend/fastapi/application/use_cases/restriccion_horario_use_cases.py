from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import RestriccionHorario, RestriccionHorarioCreate, User
from infrastructure.repositories.restriccion_horario_repository import RestriccionHorarioRepository
from infrastructure.repositories.docente_repository import DocenteRepository

class RestriccionHorarioUseCases:
    def __init__(self, restriccion_horario_repository: RestriccionHorarioRepository, docente_repository: DocenteRepository = None):
        self.restriccion_horario_repository = restriccion_horario_repository
        self.docente_repository = docente_repository

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

    # =====================================
    # MÉTODOS PARA DOCENTES AUTENTICADOS
    # =====================================

    def _get_docente_id_from_user(self, user: User) -> int:
        """Obtener el docente_id a partir del usuario autenticado con validaciones robustas"""
        if not self.docente_repository:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Repositorio de docentes no configurado"
            )
        
        # Verificar que el usuario está activo
        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo. No puede gestionar restricciones de horario"
            )
        
        # Verificar que el usuario tiene rol de docente
        if user.rol != "docente":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los docentes pueden gestionar sus restricciones de horario"
            )
        
        # Buscar el perfil de docente asociado al usuario
        docente = self.docente_repository.get_by_user_id(user.id)
        if not docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de docente no encontrado. Contacte al administrador para crear su perfil de docente"
            )
        
        return docente.id

    def get_by_docente_user(self, user: User, skip: int = 0, limit: int = 100) -> List[RestriccionHorario]:
        """Obtener restricciones de horario del docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        return self.restriccion_horario_repository.get_by_docente_with_pagination(docente_id, skip, limit)

    def get_by_id_and_docente_user(self, restriccion_id: int, user: User) -> RestriccionHorario:
        """Obtener restricción de horario por ID verificando que pertenezca al docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        restriccion = self.restriccion_horario_repository.get_by_id(restriccion_id)
        
        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción de horario no encontrada"
            )
        
        if restriccion.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede acceder a restricciones de horario de otros docentes"
            )
        
        return restriccion

    def create_for_docente_user(self, restriccion_data: RestriccionHorarioCreate, user: User) -> RestriccionHorario:
        """Crear una nueva restricción de horario para el docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        
        # Validar que no se intente asignar la restricción a otro docente
        if hasattr(restriccion_data, 'docente_id') and restriccion_data.docente_id and restriccion_data.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede crear restricciones de horario para otros docentes"
            )
        
        # Asegurar que la restricción se asocie al docente autenticado
        restriccion_data.docente_id = docente_id
        
        # Verificar si ya existe una restricción similar para el mismo docente y horario
        restricciones_existentes = self.restriccion_horario_repository.get_by_docente_y_horario(
            docente_id,
            restriccion_data.dia_semana,
            restriccion_data.hora_inicio,
            restriccion_data.hora_fin
        )
        
        if restricciones_existentes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una restricción de horario para este día y horario"
            )
        
        return self.restriccion_horario_repository.create(restriccion_data)

    def update_for_docente_user(self, restriccion_id: int, user: User, **update_data) -> RestriccionHorario:
        """Actualizar una restricción de horario verificando que pertenezca al docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        
        # Verificar que la restricción existe y pertenece al docente
        existing_restriccion = self.restriccion_horario_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción de horario no encontrada"
            )
        
        if existing_restriccion.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede modificar restricciones de horario de otros docentes"
            )
        
        # Validar que no se intente cambiar el docente_id
        if 'docente_id' in update_data and update_data['docente_id'] != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede transferir restricciones de horario a otros docentes"
            )
        
        # Si se actualizan día, hora_inicio o hora_fin, verificar que no cause duplicación
        if any(field in update_data for field in ['dia_semana', 'hora_inicio', 'hora_fin']):
            nuevo_dia = update_data.get('dia_semana', existing_restriccion.dia_semana)
            nueva_hora_inicio = update_data.get('hora_inicio', existing_restriccion.hora_inicio)
            nueva_hora_fin = update_data.get('hora_fin', existing_restriccion.hora_fin)
            
            restricciones_existentes = self.restriccion_horario_repository.get_by_docente_y_horario(
                docente_id, nuevo_dia, nueva_hora_inicio, nueva_hora_fin
            )
            
            for restriccion_existente in restricciones_existentes:
                if restriccion_existente.id != restriccion_id:  # No comparar consigo misma
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe otra restricción de horario para el día {nuevo_dia} en el horario {nueva_hora_inicio}-{nueva_hora_fin}"
                    )
        
        updated_restriccion = self.restriccion_horario_repository.update(restriccion_id, update_data)
        if not updated_restriccion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la restricción de horario"
            )
        return updated_restriccion

    def delete_for_docente_user(self, restriccion_id: int, user: User) -> bool:
        """Eliminar una restricción de horario verificando que pertenezca al docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        
        # Verificar que la restricción existe y pertenece al docente
        existing_restriccion = self.restriccion_horario_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción de horario no encontrada"
            )
        
        if existing_restriccion.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede eliminar restricciones de horario de otros docentes"
            )
        
        success = self.restriccion_horario_repository.delete(restriccion_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la restricción de horario"
            )
        return success

    def get_disponibilidad_docente_user(self, user: User, dia_semana: int = None) -> List[RestriccionHorario]:
        """Obtener disponibilidad del docente autenticado (solo restricciones marcadas como disponibles)"""
        docente_id = self._get_docente_id_from_user(user)
        return self.restriccion_horario_repository.get_disponibilidad_docente(docente_id, dia_semana)
