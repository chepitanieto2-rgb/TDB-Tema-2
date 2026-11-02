# ============================================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ============================================================

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import SessionLocal



app = FastAPI(
    title="API de Estudiantes",
    description="API REST desarrollada con Python, FastAPI, "
                "SQLAlchemy ORM y PostgreSQL",
    version="1.0.0"
)

# ============================================================
# 3. CONEXIÓN CON LA BASE DE DATOS
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# ============================================================
# 4. GET - PÁGINA PRINCIPAL
# ============================================================


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Estudiantes",
        "estado": "Servidor funcionando correctamente"
    }


# ============================================================
# 5. POST - CREAR ESTUDIANTE
# ============================================================


@app.post(
    "/estudiantes",
    response_model=schemas.EstudianteRespuesta,
    status_code=201
)
def crear_estudiante(
    estudiante: schemas.EstudianteCrear,
    db: Session = Depends(get_db)
):

    nuevo_estudiante = models.Estudiante(
        **estudiante.model_dump()
    )

    db.add(nuevo_estudiante)

    try:
        db.commit()
        db.refresh(nuevo_estudiante)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="La matrícula o el correo ya están registrados"
        )

    return nuevo_estudiante


# ============================================================
# 6. GET - CONSULTAR TODOS LOS ESTUDIANTES
# ============================================================


@app.get(
    "/estudiantes",
    response_model=list[schemas.EstudianteRespuesta]
)
def obtener_estudiantes(
    db: Session = Depends(get_db)
):

    estudiantes = db.query(
        models.Estudiante
    ).all()

    return estudiantes


# ============================================================
# 7. GET POR ID - BUSCAR UN ESTUDIANTE
# ============================================================


@app.get(
    "/estudiantes/{id}",
    response_model=schemas.EstudianteRespuesta
)
def obtener_estudiante_por_id(
    id: int,
    db: Session = Depends(get_db)
):

    estudiante = db.query(
        models.Estudiante
    ).filter(
        models.Estudiante.id == id
    ).first()

    if estudiante is None:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    return estudiante


# ============================================================
# 8. PUT - ACTUALIZAR ESTUDIANTE
# ============================================================


@app.put(
    "/estudiantes/{id}",
    response_model=schemas.EstudianteRespuesta
)
def actualizar_estudiante(
    id: int,
    datos: schemas.EstudianteCrear,
    db: Session = Depends(get_db)
):

    estudiante = db.query(
        models.Estudiante
    ).filter(
        models.Estudiante.id == id
    ).first()

    if estudiante is None:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    for campo, valor in datos.model_dump().items():
        setattr(estudiante, campo, valor)

    try:
        db.commit()
        db.refresh(estudiante)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="La matrícula o el correo ya están registrados"
        )

    return estudiante


# ============================================================
# 9. DELETE - ELIMINAR ESTUDIANTE
# ============================================================


@app.delete("/estudiantes/{id}")
def eliminar_estudiante(
    id: int,
    db: Session = Depends(get_db)
):

    estudiante = db.query(
        models.Estudiante
    ).filter(
        models.Estudiante.id == id
    ).first()

    if estudiante is None:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    db.delete(estudiante)
    db.commit()

    return {
        "mensaje": "Estudiante eliminado correctamente",
        "id_eliminado": id
    }



