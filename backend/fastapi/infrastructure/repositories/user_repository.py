from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from domain.entities import UserCreate, UserUpdate
from domain.models import User
from infrastructure.auth import AuthService


class SQLUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: UserCreate) -> User:
        """Crear un nuevo usuario"""
        # Hash de la contraseña antes de guardar
        hashed_password = AuthService.get_password_hash(user.contrasena)

        # Crear el objeto User con los campos correctos
        db_user = User(
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

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID con las relaciones cargadas"""
        return (
            self.session.query(User)
            .options(joinedload(User.docente))
            .options(joinedload(User.estudiante))
            .options(joinedload(User.administrador))
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email con las relaciones cargadas"""
        return (
            self.session.query(User)
            .options(joinedload(User.docente))
            .options(joinedload(User.estudiante))
            .options(joinedload(User.administrador))
            .filter(User.email == email)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtener todos los usuarios con paginación"""
        return self.session.query(User).offset(skip).limit(limit).all()

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Actualizar un usuario"""
        db_user = self.get_by_id(user_id)
        if db_user:
            update_data = user_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.session.commit()
            self.session.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        """Eliminar un usuario"""
        db_user = self.get_by_id(user_id)
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
            return True
        return False

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Autenticar usuario con email y contraseña"""
        user = self.get_by_email(email)
        if user and AuthService.verify_password(password, user.pass_hash):
            return user
        return None

    def is_active(self, user: User) -> bool:
        """Verificar si el usuario está activo"""
        return user.activo

    def get_by_rol(self, rol: str) -> List[User]:
        """Obtener usuarios por rol"""
        return self.session.query(User).filter(User.rol == rol).all()
