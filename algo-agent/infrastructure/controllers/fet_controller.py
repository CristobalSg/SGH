from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
async def run():
    """Endpoint para ejecutar FET"""
    # Lógica para ejecutar FET
    return {"message": "FET execution started"}