from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from infrastructure.database.config import get_db
from domain.entities import Seccion, SeccionCreate, SeccionBase, SeccionPatch, User
from application.use_cases.seccion_use_cases import SeccionUseCases
from infrastructure.repositories.seccion_repository import SeccionRepository
from infrastructure.dependencies import get_current_active_user, get_current_admin_user

router = APIRouter()

def get_seccion_use_cases(db: Session = Depends(get_db)) -> SeccionUseCases:
    repo = SeccionRepository(db)
    return SeccionUseCases(repo)

@router.get("/", response_model=List[Seccion], status_code=status.HTTP_200_OK, summary="Obtener secciones", tags=["secciones"])
async def get_secciones(
    current_user: User = Depends(get_current_active_user),
    use_cases: SeccionUseCases = Depends(get_seccion_use_cases)
):
    """Obtener todas las secciones"""
    try:
        secciones = use_cases.get_all()
        return secciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las secciones: {str(e)}"
        )

@router.get("/{seccion_id}", response_model=Seccion, status_code=status.HTTP_200_OK, summary="Obtener sección por ID", tags=["secciones"])
async def obtener_seccion(
    seccion_id: int = Path(..., gt=0, description="ID de la sección"),
    current_user: User = Depends(get_current_active_user),
    use_cases: SeccionUseCases = Depends(get_seccion_use_cases)
):
    """Obtener una sección específica por ID"""
    try:
        seccion = use_cases.get_by_id(seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sección con ID {seccion_id} no encontrada"
            )
        return seccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la sección: {str(e)}"
        )

@router.post("/", response_model=Seccion, status_code=status.HTTP_201_CREATED, summary="Crear nueva sección", tags=["secciones"])
async def create_seccion(
    seccion_data: SeccionCreate,
    use_cases: SeccionUseCases = Depends(get_seccion_use_cases),
    current_user: User = Depends(get_current_admin_user)
):
    """Crear una nueva sección (solo administradores)"""
    try:
        nueva_seccion = use_cases.create(seccion_data)
        return nueva_seccion
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
            detail=f"Error al crear la sección: {str(e)}"
        )

@router.put("/{seccion_id}", response_model=Seccion, status_code=status.HTTP_200_OK, summary="Actualizar sección completa", tags=["secciones"])
async def update_seccion(
    seccion_id: int = Path(..., gt=0, description="ID de la sección"),
    seccion_data: SeccionCreate = None,
    current_user: User = Depends(get_current_admin_user),
    use_cases: SeccionUseCases = Depends(get_seccion_use_cases)
):
    """Actualizar completamente una sección (solo administradores)"""
    try:
        update_data = {
            'codigo': seccion_data.codigo,
            'anio': seccion_data.anio,
            'semestre': seccion_data.semestre,
            'cupos': seccion_data.cupos,
            'asignatura_id': seccion_data.asignatura_id
        }
        
        seccion_actualizada = use_cases.update(seccion_id, **update_data)
        
        if not seccion_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sección con ID {seccion_id} no encontrada"
            )
        
        return seccion_actualizada
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
            detail=f"Error al actualizar la sección: {str(e)}"
        )

@router.patch("/{seccion_id}", response_model=Seccion, status_code=status.HTTP_200_OK, summary="Actualizar sección parcial", tags=["secciones"])
async def patch_seccion(
    seccion_data: SeccionPatch,
    seccion_id: int = Path(..., gt=0, description="ID de la sección"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: SeccionUseCases = Depends(get_seccion_use_cases)
):
    """Actualizar parcialmente una sección (solo administradores)"""
    try:
        # Filtrar solo los campos que no son None
        update_data = {k: v for k, v in seccion_data.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        seccion_actualizada = use_cases.update(seccion_id, **update_data)
        
        if not seccion_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sección con ID {seccion_id} no encontrada"
            )
        
        return seccion_actualizada
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
            detail=f"Error al actualizar la sección: {str(e)}"
        )

@router.delete("/{seccion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar sección", tags=["secciones"])
async def delete_seccion(
    seccion_id: int = Path(..., gt=0, description="ID de la sección"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: SeccionUseCases = Depends(get_seccion_use_cases)
):
    """Eliminar una sección (solo administradores)"""
    try:
        eliminado = use_cases.delete(seccion_id)
        
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sección con ID {seccion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la sección: {str(e)}"
        )