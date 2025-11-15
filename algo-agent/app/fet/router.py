from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.authorization import Permission
from app.dependencies import require_permission
from app.fet.service import FetRunResult, FetService
from app.schemas import User
from app.settings import AppSettings, get_settings
from app.database import get_db

router = APIRouter()


def get_fet_service(
    db: Session = Depends(get_db),
    settings: AppSettings = Depends(get_settings),
) -> FetService:
    return FetService(db=db, settings=settings)


@router.post(
    "/run",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=FetRunResult,
    summary="Ejecuta el algoritmo FET de punta a punta",
)
async def run_fet(
    _: User = Depends(require_permission(Permission.HORARIO_WRITE)),
    service: FetService = Depends(get_fet_service),
) -> FetRunResult:
    """
    Ejecuta el flujo completo de generación de horarios:

    1. Recolecta los datos necesarios desde la BD.
    2. Genera el archivo de entrada esperado por FET.
    3. Ejecuta el binario de FET y retorna un resumen.
    """
    return service.run()
