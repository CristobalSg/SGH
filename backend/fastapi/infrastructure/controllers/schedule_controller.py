from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from domain.entities import CreateScheduleRequest
from application.use_cases import CreateScheduleUseCase, ListUserSchedulesUseCase, UpdateScheduleStatusUseCase
from infrastructure.repositories.schedule_repository_memory import ScheduleRepositoryInMemory
from infrastructure.repositories.user_repository_memory import UserRepositoryInMemory
from typing import List

router = APIRouter(prefix="/schedules", tags=["schedules"])
schedule_repository = ScheduleRepositoryInMemory()
user_repository = UserRepositoryInMemory()

@router.post("")
def create_schedule(schedule_data: CreateScheduleRequest, user_id: UUID):
    use_case = CreateScheduleUseCase(repo=schedule_repository, user_repo=user_repository)
    try:
        schedule = use_case.execute(schedule_data=schedule_data, user_id=user_id)
        return {
            "message": "Solicitud de horario creada exitosamente",
            "schedule": {
                "id": str(schedule.id),
                "title": schedule.title,
                "description": schedule.description,
                "start_date": schedule.start_date,
                "end_date": schedule.end_date,
                "status": schedule.status,
                "created_at": schedule.created_at
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/user/{user_id}")
def list_user_schedules(user_id: UUID) -> List[dict]:
    use_case = ListUserSchedulesUseCase(repo=schedule_repository)
    schedules = use_case.execute(user_id=user_id)
    return [{
        "id": str(s.id),
        "title": s.title,
        "description": s.description,
        "start_date": s.start_date,
        "end_date": s.end_date,
        "status": s.status,
        "created_at": s.created_at,
        "updated_at": s.updated_at
    } for s in schedules]

@router.patch("/{schedule_id}/status")
def update_schedule_status(schedule_id: UUID, status: str, user_id: UUID):
    use_case = UpdateScheduleStatusUseCase(repo=schedule_repository, user_repo=user_repository)
    try:
        schedule = use_case.execute(schedule_id=schedule_id, status=status, user_id=user_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Horario no encontrado"
            )
        return {
            "message": "Estado del horario actualizado exitosamente",
            "schedule": {
                "id": str(schedule.id),
                "status": schedule.status,
                "updated_at": schedule.updated_at
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
