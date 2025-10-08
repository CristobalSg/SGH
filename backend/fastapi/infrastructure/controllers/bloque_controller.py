from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from infrastructure.database.config import get_db
from domain.entities import Bloque, BloqueCreate, BloqueBase, BloquePatch, User
from application.use_cases.bloque_use_cases import BloqueUseCases
from infrastructure.repositories.bloque_repository import BloqueRepository
from infrastructure.dependencies import get_current_active_user, get_current_admin_user

router = APIRouter()

def get_bloque_use_cases(db: Session = Depends(get_db)) -> BloqueUseCases:
    repo = BloqueRepository(db)
    return BloqueUseCases(repo)

@router.get("/", response_model=List[Bloque], status_code=status.HTTP_200_OK, summary="Obtener bloques", tags=["bloques"])
async def get_bloques(
    current_user: User = Depends(get_current_active_user),
    use_cases: BloqueUseCases = Depends(get_bloque_use_cases)
):
    """Obtener todos los bloques de horarios"""
    try:
        bloques = use_cases.get_all()
        return bloques
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los bloques: {str(e)}"
        )

@router.get("/{bloque_id}", response_model=Bloque, status_code=status.HTTP_200_OK, summary="Obtener bloque por ID", tags=["bloques"])
async def obtener_bloque(
    bloque_id: int = Path(..., gt=0, description="ID del bloque"),
    current_user: User = Depends(get_current_active_user),
    use_cases: BloqueUseCases = Depends(get_bloque_use_cases)
):
    """Obtener un bloque específico por ID"""
    try:
        bloque = use_cases.get_by_id(bloque_id)
        if not bloque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bloque con ID {bloque_id} no encontrado"
            )
        return bloque
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el bloque: {str(e)}"
        )

@router.post("/", response_model=Bloque, status_code=status.HTTP_201_CREATED, summary="Crear nuevo bloque", tags=["bloques"])
async def create_bloque(
    bloque_data: BloqueCreate,
    use_cases: BloqueUseCases = Depends(get_bloque_use_cases),
    current_user: User = Depends(get_current_admin_user)
):
    """Crear un nuevo bloque de horario (solo administradores)"""
    try:
        nuevo_bloque = use_cases.create(bloque_data)
        return nuevo_bloque
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
            detail=f"Error al crear el bloque: {str(e)}"
        )

@router.put("/{bloque_id}", response_model=Bloque, status_code=status.HTTP_200_OK, summary="Actualizar bloque completo", tags=["bloques"])
async def update_bloque(
    bloque_id: int = Path(..., gt=0, description="ID del bloque"),
    bloque_data: BloqueCreate = None,
    current_user: User = Depends(get_current_admin_user),
    use_cases: BloqueUseCases = Depends(get_bloque_use_cases)
):
    """Actualizar completamente un bloque (solo administradores)"""
    try:
        update_data = {
            'dia_semana': bloque_data.dia_semana,
            'hora_inicio': bloque_data.hora_inicio,
            'hora_fin': bloque_data.hora_fin
        }
        
        bloque_actualizado = use_cases.update(bloque_id, **update_data)
        
        if not bloque_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bloque con ID {bloque_id} no encontrado"
            )
        
        return bloque_actualizado
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
            detail=f"Error al actualizar el bloque: {str(e)}"
        )

@router.patch("/{bloque_id}", response_model=Bloque, status_code=status.HTTP_200_OK, summary="Actualizar bloque parcial", tags=["bloques"])
async def patch_bloque(
    bloque_data: BloquePatch,
    bloque_id: int = Path(..., gt=0, description="ID del bloque"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: BloqueUseCases = Depends(get_bloque_use_cases)
):
    """Actualizar parcialmente un bloque (solo administradores)"""
    try:
        # Filtrar solo los campos que no son None
        update_data = {k: v for k, v in bloque_data.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        bloque_actualizado = use_cases.update(bloque_id, **update_data)
        
        if not bloque_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bloque con ID {bloque_id} no encontrado"
            )
        
        return bloque_actualizado
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
            detail=f"Error al actualizar el bloque: {str(e)}"
        )

@router.delete("/{bloque_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar bloque", tags=["bloques"])
async def delete_bloque(
    bloque_id: int = Path(..., gt=0, description="ID del bloque"),
    current_user: User = Depends(get_current_admin_user),
    use_cases: BloqueUseCases = Depends(get_bloque_use_cases)
):
    """Eliminar un bloque (solo administradores)"""
    try:
        eliminado = use_cases.delete(bloque_id)
        
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bloque con ID {bloque_id} no encontrado"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el bloque: {str(e)}"
        )