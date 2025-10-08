from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from infrastructure.database.config import get_db
from domain.entities import Clase, ClaseCreate, ClaseBase, ClasePatch, User
from application.use_cases.clase_uses_cases import ClaseUseCases
from infrastructure.repositories.clase_repository import ClaseRepository
from infrastructure.dependencies import get_current_active_user, get_current_admin_user, get_current_docente_or_admin_user

router = APIRouter()

def get_clase_use_cases(db: Session = Depends(get_db)) -> ClaseUseCases:
    clase_repo = ClaseRepository(db)
    return ClaseUseCases(clase_repo)

@router.get("/", response_model=List[Clase], status_code=status.HTTP_200_OK, summary="Obtener clases", tags=["clases"])
async def get_clases(
    current_user: User = Depends(get_current_active_user),
    use_cases: ClaseUseCases = Depends(get_clase_use_cases)
):
    """Obtener todas las clases"""
    try:
        clases = use_cases.get_all()
        return clases
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las clases: {str(e)}"
        )

@router.get("/{clase_id}", response_model=Clase, status_code=status.HTTP_200_OK, summary="Obtener clase por ID", tags=["clases"])
async def obtener_clase(
    clase_id: int = Path(..., gt=0, description="ID de la clase"),
    current_user: User = Depends(get_current_active_user),
    use_cases: ClaseUseCases = Depends(get_clase_use_cases)
):
    """Obtener una clase específica por ID"""
    try:
        clase = use_cases.get_by_id(clase_id)
        if not clase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clase con ID {clase_id} no encontrada"
            )
        return clase
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la clase: {str(e)}"
        )

@router.post("/", response_model=Clase, status_code=status.HTTP_201_CREATED, summary="Crear nueva clase", tags=["clases"])
async def create_clase(
    clase_data: ClaseCreate,
    use_cases: ClaseUseCases = Depends(get_clase_use_cases),
    current_user: User = Depends(get_current_admin_user)
):
    """Crear una nueva clase (solo administradores)"""
    try:
        nueva_clase = use_cases.create(clase_data)
        return nueva_clase
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
            detail=f"Error al crear la clase: {str(e)}"
        )

@router.put("/{clase_id}", response_model=Clase, status_code=status.HTTP_200_OK, summary="Actualizar clase completa", tags=["clases"])
async def update_clase(
    clase_id: int = Path(..., gt=0, description="ID de la clase"),
    clase_data: ClaseCreate = None,
    current_user: User = Depends(get_current_docente_or_admin_user),
    use_cases: ClaseUseCases = Depends(get_clase_use_cases)
):
    """Actualizar completamente una clase (docentes y administradores)"""
    try:
        update_data = {
            'estado': clase_data.estado,
            'seccion_id': clase_data.seccion_id,
            'docente_id': clase_data.docente_id,
            'sala_id': clase_data.sala_id,
            'bloque_id': clase_data.bloque_id
        }
        
        clase_actualizada = use_cases.update(clase_id, **update_data)
        
        if not clase_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clase con ID {clase_id} no encontrada"
            )
        
        return clase_actualizada
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
            detail=f"Error al actualizar la clase: {str(e)}"
        )

@router.patch("/{clase_id}", response_model=Clase, status_code=status.HTTP_200_OK, summary="Actualizar clase parcial", tags=["clases"])
async def patch_clase(
    clase_data: ClasePatch,
    clase_id: int = Path(..., gt=0, description="ID de la clase"),
    current_user: User = Depends(get_current_docente_or_admin_user),
    use_cases: ClaseUseCases = Depends(get_clase_use_cases)
):
    """Actualizar parcialmente una clase (docentes y administradores)"""
    try:
        # Filtrar solo los campos que no son None
        update_data = {k: v for k, v in clase_data.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        clase_actualizada = use_cases.update(clase_id, **update_data)
        
        if not clase_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clase con ID {clase_id} no encontrada"
            )
        
        return clase_actualizada
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
            detail=f"Error al actualizar la clase: {str(e)}"
        )

@router.delete("/{clase_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar clase", tags=["clases"])
async def delete_clase(
    clase_id: int = Path(..., gt=0, description="ID de la clase"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: ClaseUseCases = Depends(get_clase_use_cases)
):
    """Eliminar una clase (solo administradores)"""
    try:
        eliminado = use_cases.delete(clase_id)
        
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clase con ID {clase_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la clase: {str(e)}"
        )