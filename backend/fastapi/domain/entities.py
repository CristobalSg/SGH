from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class Product:
    id: UUID
    name: str

    @staticmethod
    def new(name: str) -> "Product":
        return Product(id=uuid4(), name=name)
