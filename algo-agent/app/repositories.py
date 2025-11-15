from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app import models
from app.schemas import UserCreate, UserUpdate
from app.security import AuthService


class SQLUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: UserCreate) -> models.User:
        hashed_password = AuthService.get_password_hash(user.contrasena)
        db_user = models.User(
            nombre=user.nombre,
            email=user.email,
            pass_hash=hashed_password,
            rol=user.rol,
            activo=user.activo,
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int) -> Optional[models.User]:
        return (
            self.session.query(models.User)
            .options(joinedload(models.User.docente))
            .options(joinedload(models.User.estudiante))
            .options(joinedload(models.User.administrador))
            .filter(models.User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[models.User]:
        return (
            self.session.query(models.User)
            .options(joinedload(models.User.docente))
            .options(joinedload(models.User.estudiante))
            .options(joinedload(models.User.administrador))
            .filter(models.User.email == email)
            .first()
        )

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[models.User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        self.session.delete(db_user)
        self.session.commit()
        return True

    def is_active(self, user: models.User) -> bool:
        return user.activo


__all__ = ["SQLUserRepository"]
