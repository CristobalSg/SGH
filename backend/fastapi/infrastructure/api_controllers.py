from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from uuid import UUID

from application.use_cases import CreateProductUseCase
from domain.ports import ProductRepositoryPort

# Pydantic models para request/response
class ProductCreate(BaseModel):
    name: str

class ProductRead(BaseModel):
    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)

def get_products_router(repo: ProductRepositoryPort) -> APIRouter:
    router = APIRouter(prefix="/products", tags=["products"])
    create_uc = CreateProductUseCase(repo)

    @router.post("", response_model=ProductRead, status_code=201)
    def create_product(body: ProductCreate):
        return create_uc.execute(name=body.name)

    return router
