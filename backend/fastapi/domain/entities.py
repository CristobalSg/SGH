from dataclasses import dataclass
from uuid import UUID, uuid4
from pydantic import BaseModel

@dataclass
class User:
    id: UUID
    username: str
    password: str
    email: str
    role: str

    @staticmethod
    def new(username: str, password: str, email: str, role: str = "user") -> "User":
        return User(id=uuid4(), username=username, password=password, email=email, role=role)

class UserLogin(BaseModel):
    username: str
    password: str
