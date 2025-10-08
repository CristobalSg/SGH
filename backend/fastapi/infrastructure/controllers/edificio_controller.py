from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from domain.entities import Edificio, EdificioCreate
from infrastructure.dependencies import get_current_active_user
from application.use_cases.edificio_use_cases import EdificioUseCase
from sqlalchemy.orm import Session
from infrastructure.database.config import get_db
from infrastructure.repositories.edificio_repository import SQLEdificioRepository
from infrastructure.repositories.campus_repository import SQLCampusRepository

router = APIRouter()

def get_edificio_use_case(db: Session = Depends(get_db)) -> EdificioUseCase:
    edificio_repository = SQLEdificioRepository(db)
    campus_repository = SQLCampusRepository(db)
    return EdificioUseCase(edificio_repository, campus_repository)

@router.post("/", response_model=Edificio, status_code=status.HTTP_201_CREATED)
async def create_edificio(
    edificio_data: EdificioCreate,
    edificio_use_case: EdificioUseCase = Depends(get_edificio_use_case),
    current_user = Depends(get_current_active_user)
):
    """Crear un nuevo edificio"""
    try:
        edificio = edificio_use_case.create_edificio(edificio_data)
        return edificio
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/", response_model=List[Edificio])
async def get_all_edificios(
    edificio_use_case: EdificioUseCase = Depends(get_edificio_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener todos los edificios"""
    try:
        edificios = edificio_use_case.get_all_edificios()
        return edificios
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/{edificio_id}", response_model=Edificio)
async def get_edificio_by_id(
    edificio_id: int,
    edificio_use_case: EdificioUseCase = Depends(get_edificio_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener edificio por ID"""
    try:
        edificio = edificio_use_case.get_edificio_by_id(edificio_id)
        return edificio
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/campus/{campus_id}", response_model=List[Edificio])
async def get_edificios_by_campus(
    campus_id: int,
    edificio_use_case: EdificioUseCase = Depends(get_edificio_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener edificios por campus"""
    try:
        edificios = edificio_use_case.get_edificios_by_campus(campus_id)
        return edificios
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put("/{edificio_id}", response_model=Edificio, status_code=status.HTTP_200_OK)
async def update_edificio(
    edificio_id: int,
    edificio_data: EdificioCreate,
    edificio_use_case: EdificioUseCase = Depends(get_edificio_use_case),
    current_user = Depends(get_current_active_user)
):
    """Actualizar un edificio completo"""
    try:
        edificio = edificio_use_case.update_edificio(edificio_id, edificio_data)
        return edificio
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/{edificio_id}")
async def delete_edificio(
    edificio_id: int,
    edificio_use_case: EdificioUseCase = Depends(get_edificio_use_case),
    current_user = Depends(get_current_active_user)
):
    """Eliminar un edificio"""
    try:
        success = edificio_use_case.delete_edificio(edificio_id)
        return {"message": "Edificio eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )