
from database import Base, engine
from models import Estudiante

print("Creando tablas en PostgreSQL...")

Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")
