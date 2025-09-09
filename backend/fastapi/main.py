from fastapi import FastAPI, status
from infrastructure.controllers.test_db_controller import router as test_db_router
from infrastructure.controllers.restriccion_controller import router as restriccion_router

app = FastAPI(title="Gestión de Horarios API", version="0.1.0")

# Incluir endpoints de usuarios y horarios
app.include_router(test_db_router, prefix="/db", tags=["database"])
app.include_router(restriccion_router, prefix="/restricciones", tags=["restricciones"])

@app.get("/health", status_code=status.HTTP_200_OK, summary="Verificar estado de la API")
def health():
    return {
        "status": "ok",
        "message": "API funcionando correctamente",
        "service": "Gestión de Horarios API",
        "version": "0.1.0"
    }
