from fastapi import APIRouter

from app.fet.router import router as fet_router
from app.timetable_router import router as timetable_router

api_router = APIRouter()
api_router.include_router(fet_router, prefix="/fet", tags=["fet"])
api_router.include_router(timetable_router, prefix="/timetable", tags=["timetable"])

__all__ = ["api_router"]
