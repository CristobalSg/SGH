from fastapi import FastAPI
from infrastructure.controllers.user_controller import router as user_router
from infrastructure.controllers.schedule_controller import router as schedule_router

app = FastAPI(title="Gestión de Horarios API", version="0.1.0")

# Incluir endpoints de usuarios y horarios
app.include_router(user_router)
app.include_router(schedule_router)

@app.get("/health")
def health():
    return {"status": "ok"}
