from fastapi import FastAPI, Depends
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker, Session
#from infrastructure.sql_repository import Base, SQLProductRepository
from infrastructure.api_controllers import get_products_router
from infrastructure.dummy_repository import DummyProductRepository

# Ajusta estos valores cuando tu compañero tenga la DB lista
#DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/horariosdb"

# Configuración SQLAlchemy
#engine = create_engine(DATABASE_URL, echo=True)
#SessionLocal = sessionmaker(bind=engine)


# Intentar crear tablas si la base de datos está disponible
#try:
#   Base.metadata.create_all(bind=engine)
#except Exception as e:
#    print(f"[AVISO] No se pudo conectar a la base de datos: {e}\nLa API seguirá funcionando, pero la base de datos no está disponible.")


app = FastAPI(title="Gestión de Horarios API", version="0.1.0")

# Instanciar el repositorio dummy para desarrollo
dummy_repo = DummyProductRepository()

# Dependencia para obtener sesión
#def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()

# Inyectar repositorio con la sesión en cada request
#def get_repo(db: Session = Depends(get_db)):
#    return SQLProductRepository(db)


# Incluir endpoints usando el repositorio dummy
app.include_router(get_products_router(dummy_repo))

@app.get("/health")
def health():
    return {"status": "ok"}
