from typing import List, Optional
from uuid import UUID
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import DeclarativeBase, Session
from domain.entities import Product
from domain.ports import ProductRepositoryPort

class Base(DeclarativeBase):
    pass

class ProductTable(Base):
    __tablename__ = "products"
    id = Column(pgUUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)

class SQLProductRepository(ProductRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product) -> Product:
        row = ProductTable(id=product.id, name=product.name)
        self.session.add(row)
        self.session.commit()
        return product

    def get(self, product_id: UUID) -> Optional[Product]:
        row = self.session.get(ProductTable, product_id)
        if not row:
            return None
        return Product(id=row.id, name=row.name)

    def list(self) -> List[Product]:
        rows = self.session.query(ProductTable).all()
        return [Product(id=row.id, name=row.name) for row in rows]
