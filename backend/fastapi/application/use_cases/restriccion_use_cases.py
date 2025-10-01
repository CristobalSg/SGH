from typing import Optional, List
from fastapi import HTTPException, status
from domain.entities import RestriccionCreate, Restriccion, User
from infrastructure.repositories.restriccion_repository import RestriccionRepository
from infrastructure.repositories.docente_repository import DocenteRepository

class RestriccionUseCases:
    def __init__(self, restriccion_repository: RestriccionRepository, docente_repository: DocenteRepository = None):
        self.restriccion_repository = restriccion_repository
        self.docente_repository = docente_repository

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Restriccion]:
        """Obtener todas las restricciones con paginación"""
        return self.restriccion_repository.get_all(skip=skip, limit=limit)

    def get_by_id(self, restriccion_id: int) -> Restriccion:
        """Obtener restricción por ID"""
        restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        return restriccion

    def create(self, restriccion_data: RestriccionCreate) -> Restriccion:
        """Crear una nueva restricción"""
        return self.restriccion_repository.create(restriccion_data)

    def update(self, restriccion_id: int, **update_data) -> Restriccion:
        """Actualizar una restricción"""
        # Verificar que la restricción existe
        existing_restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        
        updated_restriccion = self.restriccion_repository.update(restriccion_id, update_data)
        if not updated_restriccion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la restricción"
            )
        return updated_restriccion

    def delete(self, restriccion_id: int) -> bool:
        """Eliminar una restricción"""
        # Verificar que la restricción existe
        existing_restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        
        success = self.restriccion_repository.delete(restriccion_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la restricción"
            )
        return success

    def get_by_docente(self, docente_id: int) -> List[Restriccion]:
        """Obtener restricciones de un docente específico"""
        return self.restriccion_repository.get_by_docente(docente_id)

    def get_by_tipo(self, tipo: str) -> List[Restriccion]:
        """Obtener restricciones por tipo"""
        return self.restriccion_repository.get_by_tipo(tipo)

    def get_by_prioridad(self, prioridad_min: int = None, prioridad_max: int = None) -> List[Restriccion]:
        """Obtener restricciones por rango de prioridad"""
        return self.restriccion_repository.get_by_prioridad(prioridad_min, prioridad_max)

    def delete_by_docente(self, docente_id: int) -> int:
        """Eliminar todas las restricciones de un docente"""
        return self.restriccion_repository.delete_by_docente(docente_id)

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
                detail="Usuario inactivo. No puede gestionar restricciones"
            )
        
        # Verificar que el usuario tiene rol de docente
        if user.rol != "docente":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los docentes pueden gestionar restricciones"
            )
        
        # Buscar el perfil de docente asociado al usuario
        docente = self.docente_repository.get_by_user_id(user.id)
        if not docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de docente no encontrado. Contacte al administrador para crear su perfil de docente"
            )
        
        return docente.id

    def get_by_docente_user(self, user: User) -> List[Restriccion]:
        """Obtener restricciones del docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        return self.restriccion_repository.get_by_docente(docente_id)

    def get_by_id_and_docente_user(self, restriccion_id: int, user: User) -> Restriccion:
        """Obtener restricción por ID verificando que pertenezca al docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        
        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        
        if restriccion.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada o no pertenece al docente"
            )
        
        return restriccion

    def create_for_docente_user(self, restriccion_data: RestriccionCreate, user: User) -> Restriccion:
        """Crear una nueva restricción para el docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        
        # Validar que no se intente asignar la restricción a otro docente
        if hasattr(restriccion_data, 'docente_id') and restriccion_data.docente_id and restriccion_data.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede crear restricciones para otros docentes"
            )
        
        # Asegurar que la restricción se asocie al docente autenticado
        restriccion_data.docente_id = docente_id
        
        # Validar datos de la restricción
        if not restriccion_data.tipo or not restriccion_data.tipo.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de restricción es obligatorio"
            )
        
        if not restriccion_data.valor or not restriccion_data.valor.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El valor de la restricción es obligatorio"
            )
        
        # Verificar que no sea una restricción duplicada
        restricciones_existentes = self.restriccion_repository.get_by_docente(docente_id)
        for restriccion_existente in restricciones_existentes:
            if (restriccion_existente.tipo == restriccion_data.tipo.lower() and 
                restriccion_existente.valor == restriccion_data.valor.strip() and
                restriccion_existente.activa):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe una restricción activa del tipo '{restriccion_data.tipo}' con valor '{restriccion_data.valor}'"
                )
        
        return self.restriccion_repository.create(restriccion_data)

    def update_for_docente_user(self, restriccion_id: int, user: User, **update_data) -> Restriccion:
        """Actualizar una restricción verificando que pertenezca al docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        
        # Verificar que la restricción existe y pertenece al docente
        existing_restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        
        if existing_restriccion.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede modificar restricciones de otros docentes"
            )
        
        # Validar que no se intente cambiar el docente_id
        if 'docente_id' in update_data and update_data['docente_id'] != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede transferir restricciones a otros docentes"
            )
        
        # Validar datos si se están actualizando
        if 'tipo' in update_data and (not update_data['tipo'] or not update_data['tipo'].strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de restricción no puede estar vacío"
            )
        
        if 'valor' in update_data and (not update_data['valor'] or not update_data['valor'].strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El valor de la restricción no puede estar vacío"
            )
        
        # Si se actualizan tipo o valor, verificar que no cause duplicación
        if 'tipo' in update_data or 'valor' in update_data:
            nuevo_tipo = update_data.get('tipo', existing_restriccion.tipo)
            nuevo_valor = update_data.get('valor', existing_restriccion.valor)
            
            restricciones_existentes = self.restriccion_repository.get_by_docente(docente_id)
            for restriccion_existente in restricciones_existentes:
                if (restriccion_existente.id != restriccion_id and  # No comparar consigo misma
                    restriccion_existente.tipo == nuevo_tipo.lower() if isinstance(nuevo_tipo, str) else nuevo_tipo and 
                    restriccion_existente.valor == nuevo_valor.strip() if isinstance(nuevo_valor, str) else nuevo_valor and
                    restriccion_existente.activa):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe otra restricción activa del tipo '{nuevo_tipo}' con valor '{nuevo_valor}'"
                    )
        
        updated_restriccion = self.restriccion_repository.update(restriccion_id, update_data)
        if not updated_restriccion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la restricción"
            )
        return updated_restriccion

    def delete_for_docente_user(self, restriccion_id: int, user: User) -> bool:
        """Eliminar una restricción verificando que pertenezca al docente autenticado"""
        docente_id = self._get_docente_id_from_user(user)
        
        # Verificar que la restricción existe y pertenece al docente
        existing_restriccion = self.restriccion_repository.get_by_id(restriccion_id)
        if not existing_restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada"
            )
        
        if existing_restriccion.docente_id != docente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede eliminar restricciones de otros docentes"
            )
        
        # Verificar si la restricción está siendo utilizada (aquí podrías agregar lógica adicional)
        # Por ejemplo, verificar si hay clases programadas que dependen de esta restricción
        
        success = self.restriccion_repository.delete(restriccion_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la restricción"
            )
        return success
