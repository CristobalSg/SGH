"""
Controlador para recuperación de contraseñas.

Endpoints seguros implementando OWASP best practices:
- Rate limiting estricto
- Prevención de enumeración de usuarios
- Validación exhaustiva de entrada
- Logging de seguridad
- Protección contra fuerza bruta
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Request, status

from application.use_cases.password_reset_use_case import PasswordResetUseCase
from domain.schemas import (
    PasswordResetRequestSchema,
    PasswordResetConfirmSchema,
    PasswordResetResponseSchema,
    PasswordResetSuccessSchema
)
from infrastructure.dependencies import get_password_reset_use_case

router = APIRouter()
logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    """
    Obtener IP del cliente considerando proxies.
    
    Args:
        request: Request de FastAPI
    
    Returns:
        IP del cliente
    """
    # Verificar headers de proxy (común en despliegues con nginx, load balancers, etc.)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Tomar la primera IP (cliente original)
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback a la IP directa
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> Optional[str]:
    """
    Obtener User-Agent del cliente.
    
    Args:
        request: Request de FastAPI
    
    Returns:
        User agent o None
    """
    return request.headers.get("User-Agent")


@router.post(
    "/password-reset/request",
    response_model=PasswordResetResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Solicitar recuperación de contraseña",
    description="""
    Solicita un link de recuperación de contraseña por email.
    
    **Características de seguridad:**
    - Rate limiting: máximo 3 intentos por email en 60 minutos
    - Rate limiting: máximo 10 intentos por IP en 60 minutos
    - Prevención de enumeración: siempre retorna mensaje genérico de éxito
    - Tokens seguros de un solo uso con expiración de 1 hora
    - Auditoría completa de todos los intentos
    
    **Respuesta:**
    Siempre retorna el mismo mensaje exitoso, independientemente de si el 
    email existe o no en el sistema. Esto previene que atacantes puedan 
    enumerar usuarios válidos.
    
    **Rate Limiting:**
    Si se excede el límite de intentos, se retornará error 429.
    """,
    tags=["Autenticación"],
)
async def request_password_reset(
    request_data: PasswordResetRequestSchema,
    request: Request,
    password_reset_use_case: PasswordResetUseCase = Depends(get_password_reset_use_case),
):
    """
    Solicitar recuperación de contraseña.
    
    Envía un email con un link para restablecer la contraseña si el email existe.
    Siempre retorna respuesta exitosa para prevenir enumeración de usuarios.
    """
    client_ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    logger.info(
        f"Solicitud de recuperación de contraseña para {request_data.email} desde IP {client_ip}"
    )
    
    return password_reset_use_case.request_password_reset(
        request_data=request_data,
        client_ip=client_ip,
        user_agent=user_agent
    )


@router.post(
    "/password-reset/confirm",
    response_model=PasswordResetSuccessSchema,
    status_code=status.HTTP_200_OK,
    summary="Confirmar recuperación de contraseña",
    description="""
    Confirma la recuperación de contraseña usando el token recibido por email.
    
    **Características de seguridad:**
    - Token de un solo uso
    - Expiración automática después de 1 hora
    - Validación estricta de contraseña (12+ caracteres, mayúsculas, minúsculas, números, especiales)
    - Invalidación automática de otros tokens del usuario
    - Tokens hasheados en base de datos
    
    **Requisitos de contraseña:**
    - Mínimo 12 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    - Al menos un carácter especial
    - No puede ser una contraseña común
    
    **Errores comunes:**
    - 400: Token inválido o expirado
    - 400: Contraseña no cumple requisitos de seguridad
    """,
    tags=["Autenticación"],
)
async def confirm_password_reset(
    confirm_data: PasswordResetConfirmSchema,
    request: Request,
    password_reset_use_case: PasswordResetUseCase = Depends(get_password_reset_use_case),
):
    """
    Confirmar recuperación de contraseña con token y nueva contraseña.
    
    Valida el token y establece la nueva contraseña si todo es correcto.
    """
    client_ip = get_client_ip(request)
    
    logger.info(f"Confirmación de recuperación de contraseña desde IP {client_ip}")
    
    return password_reset_use_case.confirm_password_reset(
        confirm_data=confirm_data,
        client_ip=client_ip
    )
