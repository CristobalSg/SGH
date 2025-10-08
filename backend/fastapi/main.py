from config import settings
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.controllers.user_controller import router as user_router
from infrastructure.controllers.auth_controller import router as auth_router
from infrastructure.controllers.test_db_controller import router as test_db_router
from infrastructure.controllers.restriccion_controller import router as restriccion_router
from infrastructure.controllers.restriccion_horario_controller import router as restriccion_horario_router
from infrastructure.controllers.docente_controller import router as docente_router
from infrastructure.controllers.edificio_controller import router as edificio_router
from infrastructure.controllers.sala_controller import router as sala_router
from infrastructure.controllers.campus_controller import router as campus_router
from infrastructure.controllers.asignatura_controller import router as asignatura_router
from infrastructure.controllers.seccion_controller import router as seccion_router
from infrastructure.controllers.bloque_controller import router as bloque_router
from infrastructure.controllers.clase_controller import router as clase_router

app = FastAPI(
    title="Gestión de Horarios API", 
    version="0.1.0", 
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

# Incluir endpoints
app.include_router(test_db_router, prefix="/api/db", tags=["database"])
app.include_router(restriccion_router, prefix="/api/restricciones", tags=["restricciones"])
app.include_router(restriccion_horario_router, prefix="/api/restricciones-horario", tags=["restricciones-horario"])
app.include_router(docente_router, prefix="/api/docentes", tags=["docentes"])
app.include_router(edificio_router, prefix="/api/edificios", tags=["edificios"])
app.include_router(sala_router, prefix="/api/salas", tags=["salas"])
app.include_router(campus_router, prefix="/api/campus", tags=["campus"])
app.include_router(asignatura_router, prefix="/api/asignaturas", tags=["asignaturas"])
app.include_router(seccion_router, prefix="/api/secciones", tags=["secciones"])
app.include_router(bloque_router, prefix="/api/bloques", tags=["bloques"])
app.include_router(clase_router, prefix="/api/clases", tags=["clases"])
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])

@app.get("/api/")
def root():
    return {
        "message": "SGH Backend API",
        "version": "0.1.0",
        "environment": settings.environment
    }

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "database": "connected"
    }