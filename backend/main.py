from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from database import engine
from database import Base

import models

from sqlalchemy.orm import Session

from database import SessionLocal
from models import Socio
from schemas import SocioCreate

from fastapi import Depends

Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
def root():
    return {"mensaje": "Backend ok"}
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo está OK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.post("/socios")
def crear_socio(
    socio: SocioCreate,
    db: Session = Depends(get_db)
):
    socio_existente = (
        db.query(Socio)
        .filter(Socio.dni == socio.dni)
        .first()
    )

    if socio_existente:
        return {
            "error": "El DNI ya existe"
        }

    ultimo_socio = (
        db.query(Socio)
        .order_by(Socio.numero_socio.desc())
        .first()
    )

    if ultimo_socio:
        numero_socio = ultimo_socio.numero_socio + 1
    else:
        numero_socio = 1

    nuevo_socio = Socio(
        numero_socio=numero_socio,
        nombre=socio.nombre,
        apellido=socio.apellido,
        dni=socio.dni,
        fecha_nacimiento=socio.fecha_nacimiento
    )

    db.add(nuevo_socio)
    db.commit()
    db.refresh(nuevo_socio)

    return {
        "mensaje": "Socio creado",
        "numero_socio": numero_socio
    }

@app.get("/socios")
def listar_socios(
    db: Session = Depends(get_db)
):
    socios = db.query(Socio).all()

    return socios

@app.delete("/socios/{numero_socio}")
def eliminar_socio(
    numero_socio: int,
    db: Session = Depends(get_db)
):
    socio = (
        db.query(Socio)
        .filter(
            Socio.numero_socio == numero_socio
        )
        .first()
    )

    if not socio:
        return {
            "error": "Socio no encontrado"
        }

    db.delete(socio)
    db.commit()

    return {
        "mensaje": f"Socio {numero_socio} eliminado"
    }

@app.put("/socios/{numero_socio}")
def modificar_socio(
    numero_socio: int,
    datos: SocioCreate,
    db: Session = Depends(get_db)
):
    socio = (
        db.query(Socio)
        .filter(
            Socio.numero_socio == numero_socio
        )
        .first()
    )

    if not socio:
        return {
            "error": "Socio no encontrado"
        }

    dni_existente = (
        db.query(Socio)
        .filter(
            Socio.dni == datos.dni,
            Socio.numero_socio != numero_socio
        )
        .first()
    )

    if dni_existente:
        return {
            "error": "El DNI ya pertenece a otro socio"
        }

    socio.nombre = datos.nombre
    socio.apellido = datos.apellido
    socio.dni = datos.dni
    socio.fecha_nacimiento = datos.fecha_nacimiento

    db.commit()
    db.refresh(socio)

    return {
        "mensaje": "Socio modificado correctamente"
    }

@app.get("/socios/{numero_socio}")
def obtener_socio(
    numero_socio: int,
    db: Session = Depends(get_db)
):
    socio = (
        db.query(Socio)
        .filter(
            Socio.numero_socio == numero_socio
        )
        .first()
    )

    if not socio:
        return {
            "error": "Socio no encontrado"
        }

    return socio
