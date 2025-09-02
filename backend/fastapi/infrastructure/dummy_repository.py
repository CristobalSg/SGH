from typing import Optional, List
from uuid import UUID
from domain.entities import Product
from domain.ports import ProductRepositoryPort

class DummyProductRepository(ProductRepositoryPort):
    def __init__(self):
        self._products: List[Product] = []

    def add(self, product: Product) -> Product:
        self._products.append(product)
        return product

    def get(self, product_id: UUID) -> Optional[Product]:
        for p in self._products:
            if p.id == product_id:
                return p
        return None

    def list(self) -> List[Product]:
        return list(self._products)