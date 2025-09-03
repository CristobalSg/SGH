from fastapi import FastAPI
from infrastructure.controllers.user_controller import router as user_router

app = FastAPI(title="Gestión de Horarios API", version="0.1.0")

# Incluir endpoints de usuarios
app.include_router(user_router)

@app.get("/health")
def health():
    return {"status": "ok"}
