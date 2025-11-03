from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from domain.entities import Docente, DocenteSecureCreate
from domain.authorization import Permission  # ✅ MIGRADO  # Response models
from infrastructure.dependencies import require_permission  # ✅ MIGRADO
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

@router.post("/", response_model=Docente, status_code=status.HTTP_201_CREATED)
async def create_docente(
    docente_data: DocenteSecureCreate,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(require_permission(Permission.DOCENTE_WRITE))  # ✅ MIGRADO
):
    """Crear.*? con validaciones anti-inyección
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

@router.get("/", response_model=List[Docente])
async def get_all_docentes(
    skip: int = 0,
    limit: int = 100,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(require_permission(Permission.DOCENTE_READ))  # ✅ MIGRADO
):
    """Obtener todos los docentes (requiere permiso DOCENTE:READ)"""
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

@router.get("/{docente_id}", response_model=Docente)
async def get_docente_by_id(
    docente_id: int,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(require_permission(Permission.DOCENTE_READ))  # ✅ MIGRADO
):
    """Obtener docente por ID (requiere permiso DOCENTE:READ)"""
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

@router.get("/departamento/{departamento}", response_model=List[Docente])
async def get_docentes_by_departamento(
    departamento: str,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(require_permission(Permission.DOCENTE_READ))  # ✅ MIGRADO
):
    """Obtener docentes por departamento (requiere permiso DOCENTE:READ)"""
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

@router.delete("/{docente_id}")
async def delete_docente(
    docente_id: int,
    docente_use_case: DocenteUseCases = Depends(get_docente_use_case),
    current_user = Depends(require_permission(Permission.DOCENTE_DELETE))  # ✅ MIGRADO
):
    """Eliminar un docente (requiere permiso DOCENTE:DELETE)"""
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