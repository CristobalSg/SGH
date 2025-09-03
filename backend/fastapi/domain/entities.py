from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime
from typing import List
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

@dataclass
class ScheduleRequirement:
    id: UUID
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    user_id: UUID
    status: str  # 'pending', 'approved', 'rejected'
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def new(title: str, description: str, start_date: datetime, end_date: datetime, user_id: UUID) -> "ScheduleRequirement":
        return ScheduleRequirement(
            id=uuid4(),
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

class CreateScheduleRequest(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
