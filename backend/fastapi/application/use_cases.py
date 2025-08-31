from dataclasses import dataclass
from domain.entities import Product
from domain.ports import ProductRepositoryPort

@dataclass
class CreateProductUseCase:
    repo: ProductRepositoryPort
    def execute(self, name: str) -> Product:
        product = Product.new(name=name)
        return self.repo.add(product)

