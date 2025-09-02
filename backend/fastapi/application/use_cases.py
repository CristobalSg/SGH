from dataclasses import dataclass
from typing import Optional
from domain.entities import User, UserLogin
from domain.ports import UserRepositoryPort

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

