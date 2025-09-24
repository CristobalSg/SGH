from config import settings
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.controllers.user_controller import router as user_router
from infrastructure.controllers.auth_controller import router as auth_router
from infrastructure.controllers.test_db_controller import router as test_db_router
from infrastructure.controllers.restriccion_controller import router as restriccion_router
from infrastructure.controllers.restriccion_horario_controller import router as restriccion_horario_router

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
app.include_router(restriccion_horario_router, prefix="/restricciones-horario", tags=["restricciones-horario"])
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])

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