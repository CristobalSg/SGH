from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
from infrastructure.database.config import get_db
from domain.entities import Restriccion, RestriccionCreate, RestriccionBase, RestriccionPatch
from application.use_cases.restriccion_use_cases import RestriccionUseCases
from infrastructure.repositories.sql_repository import SQLRestriccionRepository

router = APIRouter(tags=["restricciones"])

def get_restriccion_use_cases(db: Session = Depends(get_db)) -> RestriccionUseCases:
    repo = SQLRestriccionRepository(db)
    return RestriccionUseCases(repo)

@router.get("/", response_model=List[Restriccion], status_code=status.HTTP_200_OK, summary="Obtener todas las restricciones")
async def get_restricciones(
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    try:
        restricciones = use_cases.get_all()
        return restricciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las restricciones: {str(e)}"
        )

@router.get("/{restriccion_id}", response_model=Restriccion, status_code=status.HTTP_200_OK, summary="Obtener restricción por ID")
async def get_restriccion(
    restriccion_id: int = Path(..., gt=0, description="ID de la restricción (debe ser positivo)"),
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
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
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la restricción: {str(e)}"
        )

@router.put("/{restriccion_id}", response_model=Restriccion, status_code=status.HTTP_200_OK, summary="Actualizar restricción completa")
async def update_restriccion_complete(
    restriccion_data: RestriccionBase,
    restriccion_id: int = Path(..., gt=0, description="ID de la restricción (debe ser positivo)"),
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
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
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la restricción: {str(e)}"
        )

@router.patch("/{restriccion_id}", response_model=Restriccion, summary="Actualizar restricción parcial")
async def update_restriccion_partial(
    restriccion_data: RestriccionPatch,
    restriccion_id: int = Path(..., gt=0, description="ID de la restricción (debe ser positivo)"),
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):
    try:
        # Validar que se envíen datos usando el modelo Pydantic
        update_data = restriccion_data.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No se proporcionaron datos para actualizar"
            )
        
        restriccion_actualizada = use_cases.update(
            id=restriccion_id,
            tipo=update_data.get("tipo"),
            valor=update_data.get("valor"),
            prioridad=update_data.get("prioridad"),
            restriccion_blanda=update_data.get("restriccion_blanda"),
            restriccion_dura=update_data.get("restriccion_dura")
        )
        
        if not restriccion_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restricción con ID {restriccion_id} no encontrada"
            )
        
        return restriccion_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la restricción: {str(e)}"
        )

@router.delete("/{restriccion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar restricción")
async def delete_restriccion(
    restriccion_id: int = Path(..., gt=0, description="ID de la restricción (debe ser positivo)"),
    use_cases: RestriccionUseCases = Depends(get_restriccion_use_cases)
):

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
