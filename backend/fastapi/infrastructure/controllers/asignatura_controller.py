from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from infrastructure.database.config import get_db
from domain.entities import Asignatura, AsignaturaCreate, AsignaturaBase, AsignaturaPatch, User
from application.use_cases.asignatura_use_cases import AsignaturaUseCases
from infrastructure.repositories.asignatura_repository import AsignaturaRepository
from infrastructure.dependencies import get_current_active_user, get_current_admin_user

router = APIRouter()

def get_asignatura_use_cases(db: Session = Depends(get_db)) -> AsignaturaUseCases:
    repo = AsignaturaRepository(db)
    return AsignaturaUseCases(repo)

@router.get("/", response_model=List[Asignatura], status_code=status.HTTP_200_OK, summary="Obtener asignaturas", tags=["asignaturas"])
async def get_asignaturas(
    current_user: User = Depends(get_current_active_user),
    use_cases: AsignaturaUseCases = Depends(get_asignatura_use_cases)
):
    """Obtener todas las asignaturas"""
    try:
        asignaturas = use_cases.get_all()
        return asignaturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las asignaturas: {str(e)}"
        )

@router.get("/{asignatura_id}", response_model=Asignatura, status_code=status.HTTP_200_OK, summary="Obtener asignatura por ID", tags=["asignaturas"])
async def obtener_asignatura(
    asignatura_id: int = Path(..., gt=0, description="ID de la asignatura"),
    current_user: User = Depends(get_current_active_user),
    use_cases: AsignaturaUseCases = Depends(get_asignatura_use_cases)
):
    """Obtener una asignatura específica por ID"""
    try:
        asignatura = use_cases.get_by_id(asignatura_id)
        if not asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignatura con ID {asignatura_id} no encontrada"
            )
        return asignatura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la asignatura: {str(e)}"
        )

@router.post("/", response_model=Asignatura, status_code=status.HTTP_201_CREATED, summary="Crear nueva asignatura", tags=["asignaturas"])
async def create_asignatura(
    asignatura_data: AsignaturaCreate,
    use_cases: AsignaturaUseCases = Depends(get_asignatura_use_cases),
    current_user: User = Depends(get_current_admin_user)
):
    """Crear una nueva asignatura (solo administradores)"""
    try:
        nueva_asignatura = use_cases.create(asignatura_data)
        return nueva_asignatura
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
            detail=f"Error al crear la asignatura: {str(e)}"
        )

@router.put("/{asignatura_id}", response_model=Asignatura, status_code=status.HTTP_200_OK, summary="Actualizar asignatura completa", tags=["asignaturas"])
async def update_asignatura(
    asignatura_id: int = Path(..., gt=0, description="ID de la asignatura"),
    asignatura_data: AsignaturaCreate = None,
    current_user: User = Depends(get_current_admin_user),
    use_cases: AsignaturaUseCases = Depends(get_asignatura_use_cases)
):
    """Actualizar completamente una asignatura (solo administradores)"""
    try:
        update_data = {
            'codigo': asignatura_data.codigo,
            'nombre': asignatura_data.nombre,
            'creditos': asignatura_data.creditos
        }
        
        asignatura_actualizada = use_cases.update(asignatura_id, **update_data)
        
        if not asignatura_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignatura con ID {asignatura_id} no encontrada"
            )
        
        return asignatura_actualizada
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
            detail=f"Error al actualizar la asignatura: {str(e)}"
        )

@router.patch("/{asignatura_id}", response_model=Asignatura, status_code=status.HTTP_200_OK, summary="Actualizar asignatura parcial", tags=["asignaturas"])
async def patch_asignatura(
    asignatura_data: AsignaturaPatch,
    asignatura_id: int = Path(..., gt=0, description="ID de la asignatura"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: AsignaturaUseCases = Depends(get_asignatura_use_cases)
):
    """Actualizar parcialmente una asignatura (solo administradores)"""
    try:
        # Filtrar solo los campos que no son None
        update_data = {k: v for k, v in asignatura_data.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        asignatura_actualizada = use_cases.update(asignatura_id, **update_data)
        
        if not asignatura_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignatura con ID {asignatura_id} no encontrada"
            )
        
        return asignatura_actualizada
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
            detail=f"Error al actualizar la asignatura: {str(e)}"
        )

@router.delete("/{asignatura_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar asignatura", tags=["asignaturas"])
async def delete_asignatura(
    asignatura_id: int = Path(..., gt=0, description="ID de la asignatura"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: AsignaturaUseCases = Depends(get_asignatura_use_cases)
):
    """Eliminar una asignatura (solo administradores)"""
    try:
        eliminado = use_cases.delete(asignatura_id)
        
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignatura con ID {asignatura_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la asignatura: {str(e)}"
        )