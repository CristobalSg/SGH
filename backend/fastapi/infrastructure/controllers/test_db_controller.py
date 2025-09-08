from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database.config import get_db
from domain.models import Docente

router = APIRouter(tags=["test"])

@router.get("/test-db", summary="Probar conexión a la base de datos")
async def test_database(db: Session = Depends(get_db)):
    try:
        # Intentar hacer una consulta simple
        docente = db.query(Docente).first()
        return {
            "status": "success",
            "message": "Conexión a la base de datos exitosa",
            "data": {
                "primera_consulta": docente.__dict__ if docente else None,
                "tablas_disponibles": ["docente", "asignatura", "seccion", "sala", "bloque", "clase", "restriccion"]
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"Error de conexión: {str(e)}"}
