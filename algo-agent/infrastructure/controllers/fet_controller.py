from fastapi import APIRouter, Depends, HTTPException, status

from domain.authorization import Permission, UserRole
from infrastructure.dependencies import (
    get_user_management_use_case,
    require_permission
)

router = APIRouter()

@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
async def run(
    _: User = Depends(require_permission(Permission.HORARIO_WRITE))
):
    """Endpoint para ejecutar FET"""
    # Lógica para ejecutar FET
    return {"message": "FET execution started"}