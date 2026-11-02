
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)

    matricula = Column(
        String(20), unique=True, nullable=False
    )

    nombre = Column(String(100), nullable=False)

    apellidos = Column(String(100), nullable=False)

    carrera = Column(String(150), nullable=False)

    correo = Column(
        String(150), unique=True, nullable=False
    )

    fecha_registro = Column(
        DateTime, server_default=func.now()
    )
