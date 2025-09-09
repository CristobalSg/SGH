from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from infrastructure.database.config import get_db
from domain.entities import Restriccion, RestriccionCreate, RestriccionBase
from application.use_cases.restriccion_use_cases import RestriccionUseCases
from infrastructure.repositories.sql_repository import SQLRestriccionRepository

router = APIRouter(tags=["restricciones"])

def get_restriccion_use_cases(db: Session = Depends(get_db)) -> RestriccionUseCases:
    repo = SQLRestriccionRepository(db)
    return RestriccionUseCases(repo)

@router.get("/", response_model=List[Restriccion], summary="Obtener todas las restricciones")
async def get_restricciones(
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    """
    Obtiene todas las restricciones del sistema.
    """
    try:
        restricciones = use_cases.get_all()
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las restricciones: {str(e)}"
        )

@router.get("/{restriccion_id}", response_model=Restriccion, summary="Obtener restricción por ID")
async def get_restriccion(
    restriccion_id: int,
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    """
    Obtiene una restricción específica por su ID.
    """
    try:
        restriccion = use_cases.get_by_id(restriccion_id)
        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restricción con ID {restriccion_id} no encontrada"
            )
        return restriccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la restricción: {str(e)}"
        )

@router.post("/", response_model=Restriccion, status_code=status.HTTP_201_CREATED, summary="Crear nueva restricción")
async def create_restriccion(
    restriccion_data: RestriccionCreate,
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    """
    Crea una nueva restricción en el sistema.
    """
    try:
        nueva_restriccion = use_cases.create(
            docente_id=restriccion_data.docente_id,
            tipo=restriccion_data.tipo,
            valor=restriccion_data.valor,
            prioridad=restriccion_data.prioridad,
            restriccion_blanda=restriccion_data.restriccion_blanda,
            restriccion_dura=restriccion_data.restriccion_dura
        )
        return nueva_restriccion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la restricción: {str(e)}"
        )

@router.put("/{restriccion_id}", response_model=Restriccion, summary="Actualizar restricción completa")
async def update_restriccion_complete(
    restriccion_id: int,
    restriccion_data: RestriccionBase,
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    """
    Actualiza completamente una restricción (PUT - reemplaza todos los campos).
    """
    try:
        restriccion_actualizada = use_cases.update(
            id=restriccion_id,
            tipo=restriccion_data.tipo,
            valor=restriccion_data.valor,
            prioridad=restriccion_data.prioridad,
            restriccion_blanda=restriccion_data.restriccion_blanda,
            restriccion_dura=restriccion_data.restriccion_dura
        )
        
        if not restriccion_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restricción con ID {restriccion_id} no encontrada"
            )
        
        return restriccion_actualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la restricción: {str(e)}"
        )

@router.patch("/{restriccion_id}", response_model=Restriccion, summary="Actualizar restricción parcial")
async def update_restriccion_partial(
    restriccion_id: int,
    restriccion_data: dict,
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    """
    Actualiza parcialmente una restricción (PATCH - solo los campos proporcionados).
    """
    try:
        # Validar que solo se envíen campos permitidos
        campos_permitidos = {"tipo", "valor", "prioridad", "restriccion_blanda", "restriccion_dura"}
        campos_invalidos = set(restriccion_data.keys()) - campos_permitidos
        
        if campos_invalidos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Campos no válidos: {', '.join(campos_invalidos)}"
            )
        
        restriccion_actualizada = use_cases.update(
            id=restriccion_id,
            tipo=restriccion_data.get("tipo"),
            valor=restriccion_data.get("valor"),
            prioridad=restriccion_data.get("prioridad"),
            restriccion_blanda=restriccion_data.get("restriccion_blanda"),
            restriccion_dura=restriccion_data.get("restriccion_dura")
        )
        
        if not restriccion_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restricción con ID {restriccion_id} no encontrada"
            )
        
        return restriccion_actualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la restricción: {str(e)}"
        )

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar restricción")
async def delete_restriccion(
    restriccion_id: int,
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    """
    Elimina una restricción del sistema.
    """
    try:
        deleted = use_cases.delete(restriccion_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restricción con ID {restriccion_id} no encontrada"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la restricción: {str(e)}"
        )
