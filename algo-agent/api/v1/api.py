from fastapi import APIRouter
from api.v1.endpoints.fet import fet_router

api_router = APIRouter()

api_router.include_router(fet_router, prefix="/fet", tags=["fet"])