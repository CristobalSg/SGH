from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import api_router

app = FastAPI(
    title="SGH - Sistema de Gestión de Horarios", 
    version="1.0.0",
    description="API REST para la gestión de horarios académicos",
    docs_url="/api/docs", 
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS usando configuración centralizada
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router principal de la API v1
app.include_router(api_router, prefix="/api")

@app.get("/api/")
def root():
    return {
        "message": "SGH Backend API",
        "version": "1.0.0",
        "environment": settings.environment,
        "docs": "/api/docs"
    }

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "database": "connected"
    }
