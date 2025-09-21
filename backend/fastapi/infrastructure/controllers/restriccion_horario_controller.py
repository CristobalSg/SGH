from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from domain.entities import RestriccionHorario, RestriccionHorarioCreate, RestriccionHorarioPatch, User
from infrastructure.database.config import get_db
from infrastructure.repositories.restriccion_horario_repository import RestriccionHorarioRepository
from application.use_cases.restriccion_horario_use_cases import RestriccionHorarioUseCases
from infrastructure.dependencies import get_current_active_user

router = APIRouter()

def get_restriccion_horario_repository(db: Session = Depends(get_db)) -> RestriccionHorarioRepository:
    """Dependency para obtener el repositorio de restricciones de horario"""
    return RestriccionHorarioRepository(db)

def get_restriccion_horario_use_cases(
    repository: RestriccionHorarioRepository = Depends(get_restriccion_horario_repository)
) -> RestriccionHorarioUseCases:
    """Dependency para obtener los casos de uso de restricciones de horario"""
    return RestriccionHorarioUseCases(repository)

@router.post("/", response_model=RestriccionHorario, status_code=status.HTTP_201_CREATED)
async def crear_restriccion_horario(
    restriccion_data: RestriccionHorarioCreate,
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """Crear una nueva restricción de horario"""
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

@router.get("/", response_model=List[RestriccionHorario])
async def obtener_restricciones_horario(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a devolver"),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener todas las restricciones de horario con paginación"""
    try:
        restricciones = use_cases.get_all(skip=skip, limit=limit)
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/{restriccion_id}", response_model=RestriccionHorario)
async def obtener_restriccion_horario(
    restriccion_id: int,
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener una restricción de horario por ID"""
    try:
        restriccion = use_cases.get_by_id(restriccion_id)
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.patch("/{restriccion_id}", response_model=RestriccionHorario)
async def actualizar_restriccion_horario(
    restriccion_id: int,
    restriccion_patch: RestriccionHorarioPatch,
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar parcialmente una restricción de horario"""
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

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_restriccion_horario(
    restriccion_id: int,
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar una restricción de horario"""
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

@router.get("/docente/{docente_id}", response_model=List[RestriccionHorario])
async def obtener_restricciones_por_docente(
    docente_id: int,
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener todas las restricciones de horario de un docente específico"""
    try:
        restricciones = use_cases.get_by_docente(docente_id)
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/dia/{dia_semana}", response_model=List[RestriccionHorario])
async def obtener_restricciones_por_dia(
    dia_semana: int = Path(..., ge=0, le=6, description="Día de la semana (0=Domingo, 6=Sábado)"),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener todas las restricciones de horario para un día específico de la semana"""
    try:
        restricciones = use_cases.get_by_dia_semana(dia_semana)
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/disponibilidad/{docente_id}", response_model=List[RestriccionHorario])
async def obtener_disponibilidad_docente(
    docente_id: int,
    dia_semana: Optional[int] = Query(None, ge=0, le=6, description="Día de la semana (opcional)"),
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases)
):
    """Obtener la disponibilidad de un docente (solo restricciones marcadas como disponibles)"""
    try:
        disponibilidad = use_cases.get_disponibilidad_docente(docente_id, dia_semana)
        return disponibilidad
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.delete("/docente/{docente_id}", status_code=status.HTTP_200_OK)
async def eliminar_restricciones_por_docente(
    docente_id: int,
    use_cases: RestriccionHorarioUseCases = Depends(get_restriccion_horario_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar todas las restricciones de horario de un docente"""
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