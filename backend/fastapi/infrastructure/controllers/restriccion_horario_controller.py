from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from domain.entities import RestriccionHorario, RestriccionHorarioCreate, RestriccionHorarioPatch, User
from infrastructure.database.config import get_db
from infrastructure.repositories.restriccion_horario_repository import RestriccionHorarioRepository
from infrastructure.repositories.docente_repository import DocenteRepository
from application.use_cases.restriccion_horario_use_cases import RestriccionHorarioUseCases
from infrastructure.dependencies import get_current_active_user, get_current_admin_user, get_current_docente_user

router = APIRouter()

def get_restriccion_horario_repository(db: Session = Depends(get_db)) -> RestriccionHorarioRepository:
    """Dependency para obtener el repositorio de restricciones de horario"""
    return RestriccionHorarioRepository(db)

def get_restriccion_horario_use_cases(
    repository: RestriccionHorarioRepository = Depends(get_restriccion_horario_repository),
    db: Session = Depends(get_db)
) -> RestriccionHorarioUseCases:
    """Dependency para obtener los casos de uso de restricciones de horario"""
    docente_repo = DocenteRepository(db)
    return RestriccionHorarioUseCases(repository, docente_repo)

@router.post("/", response_model=RestriccionHorario, status_code=status.HTTP_201_CREATED, tags=["admin-restricciones-horario"])
async def crear_restriccion_horario(
    restriccion_data: RestriccionHorarioCreate,
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Crear una nueva restricción de horario (solo administradores)"""
    try:
        restriccion = use_cases.create(restriccion_data)
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/", response_model=List[RestriccionHorario], tags=["admin-restricciones-horario"])
async def obtener_restricciones_horario(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a devolver"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener todas las restricciones de horario con paginación (solo administradores)"""
    try:
        restricciones = use_cases.get_all(skip=skip, limit=limit)
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/{restriccion_id}", response_model=RestriccionHorario, tags=["admin-restricciones-horario"])
async def obtener_restriccion_horario(
    restriccion_id: int,
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener una restricción de horario por ID (solo administradores)"""
    try:
        restriccion = use_cases.get_by_id(restriccion_id)
        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restricción de horario con ID {restriccion_id} no encontrada"
            )
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.patch("/{restriccion_id}", response_model=RestriccionHorario, tags=["admin-restricciones-horario"])
async def actualizar_restriccion_horario(
    restriccion_id: int,
    restriccion_patch: RestriccionHorarioPatch,
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Actualizar parcialmente una restricción de horario (solo administradores)"""
    try:
        # Convertir a dict y filtrar valores None
        update_data = {k: v for k, v in restriccion_patch.model_dump(exclude_unset=True).items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        restriccion = use_cases.update(restriccion_id, **update_data)
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["admin-restricciones-horario"])
async def eliminar_restriccion_horario(
    restriccion_id: int,
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Eliminar una restricción de horario (solo administradores)"""
    try:
        use_cases.delete(restriccion_id)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/docente/{docente_id}", response_model=List[RestriccionHorario], tags=["admin-restricciones-horario"])
async def obtener_restricciones_por_docente(
    docente_id: int,
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener todas las restricciones de horario de un docente específico (solo administradores)"""
    try:
        restricciones = use_cases.get_by_docente(docente_id)
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/dia/{dia_semana}", response_model=List[RestriccionHorario], tags=["admin-restricciones-horario"])
async def obtener_restricciones_por_dia(
    dia_semana: int = Path(..., ge=0, le=6, description="Día de la semana (0=Domingo, 6=Sábado)"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener todas las restricciones de horario para un día específico de la semana (solo administradores)"""
    try:
        restricciones = use_cases.get_by_dia_semana(dia_semana)
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/disponibilidad/{docente_id}", response_model=List[RestriccionHorario], tags=["admin-restricciones-horario"])
async def obtener_disponibilidad_docente(
    docente_id: int,
    dia_semana: Optional[int] = Query(None, ge=0, le=6, description="Día de la semana (opcional)"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener la disponibilidad de un docente (solo restricciones marcadas como disponibles) - Solo administradores"""
    try:
        disponibilidad = use_cases.get_disponibilidad_docente(docente_id, dia_semana)
        return disponibilidad
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.delete("/docente/{docente_id}", status_code=status.HTTP_200_OK, tags=["admin-restricciones-horario"])
async def eliminar_restricciones_por_docente(
    docente_id: int,
    current_user: User = Depends(get_current_admin_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Eliminar todas las restricciones de horario de un docente (solo administradores)"""
    try:
        count = use_cases.delete_by_docente(docente_id)
        return {
            "mensaje": f"Se eliminaron {count} restricciones de horario del docente {docente_id}",
            "eliminadas": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

# =====================================
# ENDPOINTS PARA DOCENTES (SUS PROPIAS RESTRICCIONES DE HORARIO)
# =====================================

@router.get("/docente/mis-restricciones", response_model=List[RestriccionHorario], tags=["docente-restricciones-horario"])
async def docente_get_mis_restricciones_horario(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a devolver"),
    current_user: User = Depends(get_current_docente_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener las restricciones de horario del docente autenticado"""
    try:
        restricciones = use_cases.get_by_docente_user(current_user, skip=skip, limit=limit)
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.post("/docente/mis-restricciones", response_model=RestriccionHorario, status_code=status.HTTP_201_CREATED, tags=["docente-restricciones-horario"])
async def docente_crear_restriccion_horario(
    restriccion_data: RestriccionHorarioCreate,
    current_user: User = Depends(get_current_docente_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Crear una nueva restricción de horario para el docente autenticado"""
    try:
        restriccion = use_cases.create_for_docente_user(restriccion_data, current_user)
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/docente/mis-restricciones/{restriccion_id}", response_model=RestriccionHorario, tags=["docente-restricciones-horario"])
async def docente_get_restriccion_horario(
    restriccion_id: int,
    current_user: User = Depends(get_current_docente_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener una restricción de horario específica del docente autenticado"""
    try:
        restriccion = use_cases.get_by_id_and_docente_user(restriccion_id, current_user)
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.patch("/docente/mis-restricciones/{restriccion_id}", response_model=RestriccionHorario, tags=["docente-restricciones-horario"])
async def docente_actualizar_restriccion_horario(
    restriccion_id: int,
    restriccion_patch: RestriccionHorarioPatch,
    current_user: User = Depends(get_current_docente_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Actualizar una restricción de horario del docente autenticado"""
    try:
        # Convertir a dict y filtrar valores None
        update_data = {k: v for k, v in restriccion_patch.model_dump(exclude_unset=True).items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        restriccion = use_cases.update_for_docente_user(restriccion_id, current_user, **update_data)
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.delete("/docente/mis-restricciones/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["docente-restricciones-horario"])
async def docente_eliminar_restriccion_horario(
    restriccion_id: int,
    current_user: User = Depends(get_current_docente_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Eliminar una restricción de horario del docente autenticado"""
    try:
        use_cases.delete_for_docente_user(restriccion_id, current_user)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/docente/mi-disponibilidad", response_model=List[RestriccionHorario], tags=["docente-restricciones-horario"])
async def docente_get_mi_disponibilidad(
    dia_semana: Optional[int] = Query(None, ge=0, le=6, description="Día de la semana (opcional)"),
    current_user: User = Depends(get_current_docente_user),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener la disponibilidad del docente autenticado"""
    try:
        disponibilidad = use_cases.get_disponibilidad_docente_user(current_user, dia_semana)
        return disponibilidad
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )