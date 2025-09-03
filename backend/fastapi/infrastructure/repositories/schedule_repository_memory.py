from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime
from domain.entities import ScheduleRequirement
from domain.ports import ScheduleRepositoryPort

class ScheduleRepositoryInMemory(ScheduleRepositoryPort):
    def __init__(self):
        self.schedules: Dict[UUID, ScheduleRequirement] = {}

    def add(self, schedule: ScheduleRequirement) -> ScheduleRequirement:
        self.schedules[schedule.id] = schedule
        return schedule

    def get(self, schedule_id: UUID) -> Optional[ScheduleRequirement]:
        return self.schedules.get(schedule_id)

    def list(self) -> List[ScheduleRequirement]:
        return list(self.schedules.values())

    def list_by_user(self, user_id: UUID) -> List[ScheduleRequirement]:
        return [
            schedule for schedule in self.schedules.values()
            if schedule.user_id == user_id
        ]

    def update_status(self, schedule_id: UUID, status: str) -> Optional[ScheduleRequirement]:
        schedule = self.schedules.get(schedule_id)
        if schedule:
            schedule.status = status
            schedule.updated_at = datetime.now()
            return schedule
        return None
