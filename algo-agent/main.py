from fastapi import FastAPI
from api.v1.api import api_router

app = FastAPI(
    title="SGH - Sistema de Gestión de Horarios", 
    version="1.0.0",
    description="API REST para la gestión de horarios académicos",
    docs_url="/api/v1/docs", 
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")
