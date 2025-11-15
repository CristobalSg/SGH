"""
Router para generación de horarios desde JSON
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.timetable_schemas import (
    TimetableGenerationRequest,
    TimetableGenerationResponse,
)
from app.timetable_service import timetable_service, TimetableService
from app.dependencies import verify_service_token


router = APIRouter(tags=["Timetable"])


def get_timetable_service() -> TimetableService:
    """Dependency para obtener el servicio de timetable"""
    return timetable_service


@router.post(
    "/generate",
    response_model=TimetableGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generar archivo FET desde JSON",
    description=(
        "Recibe un JSON con toda la información del horario y genera "
        "un archivo FET listo para ser procesado por el algoritmo FET"
    ),
)
async def generate_timetable(
    request: TimetableGenerationRequest,
    service: TimetableService = Depends(get_timetable_service),
    _: bool = Depends(verify_service_token),
) -> TimetableGenerationResponse:
    """
    Generar archivo FET desde JSON
    
    Args:
        request: Request con toda la información del horario
        service: Servicio de timetable
        _: Validación de token de servicio
        
    Returns:
        Response con el resultado de la generación
    """
    try:
        result = service.generate_fet_file(request)
        return result

    except Exception as e:
        return TimetableGenerationResponse(
            success=False,
            message=f"Error inesperado: {str(e)}",
            timetable_id=request.metadata.timetable_id,
            file_url=None,
            errors=[str(e)],
        )
