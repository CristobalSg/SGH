from fastapi import FastAPI
from infrastructure.controllers.test_db_controller import router as test_db_router

app = FastAPI(title="Gestión de Horarios API", version="0.1.0")

# Incluir endpoints de usuarios y horarios
app.include_router(test_db_router, prefix="/db", tags=["database"])

@app.get("/health")
def health():
    return {"status": "ok"}
