
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class EstudianteBase(BaseModel):
    matricula: str
    nombre: str
    apellidos: str
    carrera: str
    correo: EmailStr

class EstudianteCrear(EstudianteBase):
    pass

class EstudianteRespuesta(EstudianteBase):
    id: int
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)
