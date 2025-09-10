from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.controllers.test_db_controller import router as test_db_router
from infrastructure.controllers.restriccion_controller import router as restriccion_router
from config import settings

app = FastAPI(title="Gestión de Horarios API", version="0.1.0")

# CORS usando configuración centralizada
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir endpoints
app.include_router(test_db_router, prefix="/db", tags=["database"])
app.include_router(restriccion_router, prefix="/restricciones", tags=["restricciones"])

@app.get("/")
def root():
    return {
        "message": "SGH Backend API",
        "version": "0.1.0",
        "environment": settings.environment
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "database": "connected"
    }