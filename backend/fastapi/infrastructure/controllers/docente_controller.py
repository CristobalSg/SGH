from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from domain.entities import Docente, DocenteCreate
from infrastructure.dependencies import get_current_active_user
from application.use_cases.docente_use_cases import DocenteUseCases
from sqlalchemy.orm import Session
from infrastructure.database.config import get_db
from infrastructure.repositories.docente_repository import DocenteRepository
from infrastructure.repositories.user_repository import SQLUserRepository

router = APIRouter()

def get_docente_use_case(db: Session = Depends(get_db)) -> DocenteUseCases:
    docente_repository = DocenteRepository(db)
    user_repository = SQLUserRepository(db)
    return DocenteUseCases(docente_repository, user_repository)

@router.post("/api/docentes", response_model=Docente, status_code=status.HTTP_201_CREATED)
async def create_docente(
    docente_data: DocenteCreate,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(get_current_active_user)
):
    """Crear un nuevo docente"""
    try:
        docente = docente_use_case.create(docente_data)
        return docente
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/api/docentes", response_model=List[Docente])
async def get_all_docentes(
    skip: int = 0,
    limit: int = 100,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener todos los docentes"""
    try:
        docentes = docente_use_case.get_all(skip=skip, limit=limit)
        return docentes
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/api/docentes/{docente_id}", response_model=Docente)
async def get_docente_by_id(
    docente_id: int,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener docente por ID"""
    try:
        docente = docente_use_case.get_by_id(docente_id)
        return docente
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/api/docentes/departamento/{departamento}", response_model=List[Docente])
async def get_docentes_by_departamento(
    departamento: str,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(get_current_active_user)
):
    """Obtener docentes por departamento"""
    try:
        docentes = docente_use_case.get_by_departamento(departamento)
        return docentes
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/api/docentes/{docente_id}")
async def delete_docente(
    docente_id: int,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(get_current_active_user)
):
    """Eliminar un docente"""
    try:
        success = docente_use_case.delete(docente_id)
        return {"message": "Docente eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )