"""
Script de bootstrap para usuarios de desarrollo (docente y estudiante).

Este script crea usuarios de ejemplo para desarrollo COMPARTIDOS por el equipo.
NO crea administradores (eso lo hace bootstrap_admin.py).

Ejecutar con: `python backend/fastapi/scripts/bootstrap_dev_users.py`
El script es idempotente: si el usuario ya existe, lo actualiza.

IMPORTANTE: Estos usuarios son VISIBLES por todo el equipo en la base de datos compartida.
"""

import logging
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

# Ajustar el PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from infrastructure.database.config import SessionLocal
from infrastructure.repositories.user_repository import SQLUserRepository
from infrastructure.repositories.docente_repository import DocenteRepository
from infrastructure.repositories.estudiante_repository import SQLEstudianteRepository
from domain.entities import UserCreate, DocenteCreate, EstudianteCreate
from infrastructure.auth import AuthService
from config import settings

logger = logging.getLogger("bootstrap_dev_users")
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s [%(name)s] %(message)s",
)


@contextmanager
def _db_session() -> Iterator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _get_optional_setting(attr_name: str, default: Optional[str] = None) -> Optional[str]:
    """Obtiene una configuración opcional desde settings."""
    value = getattr(settings, attr_name, None)
    return value if value else default


def ensure_docente_user() -> None:
    """Crea o actualiza el usuario docente para desarrollo."""
    docente_name = _get_optional_setting("dev_docente_name")
    docente_email = _get_optional_setting("dev_docente_email")
    docente_password = _get_optional_setting("dev_docente_password")
    docente_departamento = _get_optional_setting("dev_docente_departamento", "INFORMATICA")

    # Si no hay configuración, saltar
    if not docente_email:
        logger.info("No se configuró docente de desarrollo (DEV_DOCENTE_EMAIL no definida)")
        return

    if not docente_name or not docente_password:
        logger.warning(
            "Configuración incompleta para docente: requiere DEV_DOCENTE_NAME, "
            "DEV_DOCENTE_EMAIL y DEV_DOCENTE_PASSWORD"
        )
        return

    with _db_session() as session:
        user_repo = SQLUserRepository(session)
        docente_repo = DocenteRepository(session)

        user = user_repo.get_by_email(docente_email)
        
        if not user:
            try:
                # Crear usuario
                user = user_repo.create(
                    UserCreate(
                        nombre=docente_name,
                        email=docente_email,
                        rol="docente",
                        activo=True,
                        contrasena=docente_password,
                    )
                )
                logger.info(
                    "✓ Usuario docente %s creado con id %s",
                    docente_email,
                    user.id,
                )

                # Crear perfil de docente
                docente = docente_repo.create(
                    DocenteCreate(
                        user_id=user.id,
                        departamento=docente_departamento
                    )
                )
                logger.info("✓ Perfil de docente creado (ID: %s)", docente.id)

            except ValidationError as exc:
                raise RuntimeError(
                    f"Datos de docente inválidos: {exc}"
                ) from exc
        else:
            # Actualizar si cambió algo
            updated = False
            if user.nombre != docente_name:
                user.nombre = docente_name
                updated = True
            if user.rol != "docente":
                user.rol = "docente"
                updated = True
            if not AuthService.verify_password(docente_password, user.pass_hash):
                user.pass_hash = AuthService.get_password_hash(docente_password)
                updated = True

            if updated:
                session.add(user)
                logger.info("✓ Usuario docente %s actualizado", docente_email)
            else:
                logger.info("Usuario docente %s ya existe y está actualizado", docente_email)


def ensure_estudiante_user() -> None:
    """Crea o actualiza el usuario estudiante para desarrollo."""
    estudiante_name = _get_optional_setting("dev_estudiante_name")
    estudiante_email = _get_optional_setting("dev_estudiante_email")
    estudiante_password = _get_optional_setting("dev_estudiante_password")
    estudiante_matricula = _get_optional_setting("dev_estudiante_matricula", "2024001")

    # Si no hay configuración, saltar
    if not estudiante_email:
        logger.info("No se configuró estudiante de desarrollo (DEV_ESTUDIANTE_EMAIL no definida)")
        return

    if not estudiante_name or not estudiante_password:
        logger.warning(
            "Configuración incompleta para estudiante: requiere DEV_ESTUDIANTE_NAME, "
            "DEV_ESTUDIANTE_EMAIL y DEV_ESTUDIANTE_PASSWORD"
        )
        return

    with _db_session() as session:
        user_repo = SQLUserRepository(session)
        estudiante_repo = SQLEstudianteRepository(session)

        user = user_repo.get_by_email(estudiante_email)
        
        if not user:
            try:
                # Crear usuario
                user = user_repo.create(
                    UserCreate(
                        nombre=estudiante_name,
                        email=estudiante_email,
                        rol="estudiante",
                        activo=True,
                        contrasena=estudiante_password,
                    )
                )
                logger.info(
                    "✓ Usuario estudiante %s creado con id %s",
                    estudiante_email,
                    user.id,
                )

                # Crear perfil de estudiante
                estudiante = estudiante_repo.create(
                    EstudianteCreate(
                        user_id=user.id,
                        matricula=estudiante_matricula
                    )
                )
                logger.info("✓ Perfil de estudiante creado (ID: %s)", estudiante.id)

            except ValidationError as exc:
                raise RuntimeError(
                    f"Datos de estudiante inválidos: {exc}"
                ) from exc
        else:
            # Actualizar si cambió algo
            updated = False
            if user.nombre != estudiante_name:
                user.nombre = estudiante_name
                updated = True
            if user.rol != "estudiante":
                user.rol = "estudiante"
                updated = True
            if not AuthService.verify_password(estudiante_password, user.pass_hash):
                user.pass_hash = AuthService.get_password_hash(estudiante_password)
                updated = True

            if updated:
                session.add(user)
                logger.info("✓ Usuario estudiante %s actualizado", estudiante_email)
            else:
                logger.info("Usuario estudiante %s ya existe y está actualizado", estudiante_email)


def main() -> None:
    logger.info("🎓 Iniciando bootstrap de usuarios con sus roles...")
    
    try:
        ensure_docente_user()
        ensure_estudiante_user()
    except (RuntimeError, SQLAlchemyError) as exc:
        logger.error("❌ Bootstrap de usuarios con sus roles falló: %s", exc)
        raise SystemExit(1) from exc
    
    logger.info("✅ Bootstrap de usuarios con sus roles completado correctamente.")

if __name__ == "__main__":
    main()
