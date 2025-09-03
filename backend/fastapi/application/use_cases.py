from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID
from domain.entities import User, UserLogin, ScheduleRequirement, CreateScheduleRequest
from domain.ports import UserRepositoryPort, ScheduleRepositoryPort

@dataclass
class CreateUserUseCase:
    repo: UserRepositoryPort
    def execute(self, username: str, password: str, email: str, role: str = "user") -> User:
        user = User.new(username=username, password=password, email=email, role=role)
        return self.repo.add(user)

@dataclass
class LoginUseCase:
    repo: UserRepositoryPort
    def execute(self, login_data: UserLogin) -> Optional[User]:
        user = self.repo.get_by_username(login_data.username)
        if user and user.password == login_data.password:
            return user
        return None

@dataclass
class CreateScheduleUseCase:
    repo: ScheduleRepositoryPort
    user_repo: UserRepositoryPort

    def execute(self, schedule_data: CreateScheduleRequest, user_id: UUID) -> ScheduleRequirement:
        # Verificar que el usuario existe
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
            
        schedule = ScheduleRequirement.new(
            title=schedule_data.title,
            description=schedule_data.description,
            start_date=schedule_data.start_date,
            end_date=schedule_data.end_date,
            user_id=user_id
        )
        return self.repo.add(schedule)

@dataclass
class ListUserSchedulesUseCase:
    repo: ScheduleRepositoryPort

    def execute(self, user_id: UUID) -> List[ScheduleRequirement]:
        return self.repo.list_by_user(user_id)

@dataclass
class UpdateScheduleStatusUseCase:
    repo: ScheduleRepositoryPort
    user_repo: UserRepositoryPort

    def execute(self, schedule_id: UUID, status: str, user_id: UUID) -> Optional[ScheduleRequirement]:
        user = self.user_repo.get(user_id)
        if not user or user.role != "admin":
            raise ValueError("No tienes permisos para realizar esta acción")

        return self.repo.update_status(schedule_id, status)

