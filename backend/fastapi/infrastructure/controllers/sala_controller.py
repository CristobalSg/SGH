from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from domain.entities import Sala, SalaCreate
from infrastructure.dependencies import get_current_active_user
from application.use_cases.sala_use_cases import SalaUseCases
from sqlalchemy.orm import Session
from infrastructure.database.config import get_db
from infrastructure.repositories.sala_repository import SalaRepository
from infrastructure.repositories.edificio_repository import SQLEdificioRepository

router = APIRouter()

def get_sala_use_case(db: Session = Depends(get_db)) -> SalaUseCases:
    sala_repository = SalaRepository(db)
    edificio_repository = SQLEdificioRepository(db)
    return SalaUseCases(sala_repository, edificio_repository)

@router.post("/", response_model=Sala, status_code=status.HTTP_201_CREATED)
async def create_sala(
    sala_data: SalaCreate,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Crear una nueva sala"""
    try:
        sala = sala_use_case.create(sala_data)
        return sala
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/", response_model=List[Sala])
async def get_all_salas(
    skip: int = 0,
    limit: int = 100,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener todas las salas"""
    try:
        salas = sala_use_case.get_all(skip=skip, limit=limit)
        return salas
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/{sala_id}", response_model=Sala)
async def get_sala_by_id(
    sala_id: int,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener sala por ID"""
    try:
        sala = sala_use_case.get_by_id(sala_id)
        return sala
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/codigo/{codigo}", response_model=Sala)
async def get_sala_by_codigo(
    codigo: str,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener sala por código"""
    try:
        sala = sala_use_case.get_by_codigo(codigo)
        return sala
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Esta ruta debe estar en edificio_controller, pero la dejamos aquí por compatibilidad
@router.get("/edificio/{edificio_id}", response_model=List[Sala])
async def get_salas_by_edificio(
    edificio_id: int,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener salas por edificio"""
    try:
        salas = sala_use_case.get_by_edificio(edificio_id)
        return salas
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put("/{sala_id}", response_model=Sala, status_code=status.HTTP_200_OK)
async def update_sala(
    sala_id: int,
    sala_data: SalaCreate,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Actualizar una sala"""
    try:
        update_data = {
            'codigo': sala_data.codigo,
            'nombre': sala_data.nombre,
            'capacidad': sala_data.capacidad,
            'tipo': sala_data.tipo,
            'edificio_id': sala_data.edificio_id
        }
        sala = sala_use_case.update(sala_id, **update_data)
        return sala
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/{sala_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sala(
    sala_id: int,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Eliminar una sala"""
    try:
        sala_use_case.delete(sala_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/buscar/tipo/{tipo}", response_model=List[Sala])
async def get_salas_by_tipo(
    tipo: str,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener salas por tipo"""
    try:
        salas = sala_use_case.get_by_tipo(tipo)
        return salas
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/buscar/capacidad", response_model=List[Sala])
async def get_salas_by_capacidad(
    capacidad_min: int = None,
    capacidad_max: int = None,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener salas por rango de capacidad"""
    try:
        salas = sala_use_case.get_by_capacidad(capacidad_min, capacidad_max)
        return salas
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/disponibles", response_model=List[Sala])
async def get_salas_disponibles(
    bloque_id: int = None,
    sala_use_case: SalaUseCases = Depends(get_sala_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener salas disponibles, opcionalmente filtradas por bloque"""
    try:
        salas = sala_use_case.get_salas_disponibles(bloque_id)
        return salas
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )