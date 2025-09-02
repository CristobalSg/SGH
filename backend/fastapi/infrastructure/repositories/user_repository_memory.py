from typing import Optional, List, Dict
from uuid import UUID
from domain.entities import User
from domain.ports import UserRepositoryPort

class UserRepositoryInMemory(UserRepositoryPort):
    def __init__(self):
        self.users: Dict[UUID, User] = {}
        self.username_index: Dict[str, UUID] = {}

    def add(self, user: User) -> User:
        self.users[user.id] = user
        self.username_index[user.username] = user.id
        return user

    def get(self, user_id: UUID) -> Optional[User]:
        return self.users.get(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        user_id = self.username_index.get(username)
        if user_id:
            return self.users.get(user_id)
        return None

    def list(self) -> List[User]:
        return list(self.users.values())
