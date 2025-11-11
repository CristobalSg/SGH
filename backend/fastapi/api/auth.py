"""
Endpoints de autenticación y gestión de usuarios.
"""
from infrastructure.controllers.auth_controller import router as auth_router
from infrastructure.controllers.user_controller import router as user_router

__all__ = ["auth_router", "user_router"]
