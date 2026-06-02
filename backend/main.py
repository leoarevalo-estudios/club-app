
# ============================================================
# IMPORTACIONES
# ============================================================

# FastAPI: framework para crear la API
from fastapi import FastAPI, Depends

# Middleware CORS: permite que el frontend se comunique con el backend
from fastapi.middleware.cors import CORSMiddleware

# SQLAlchemy: manejo de sesiones de base de datos
from sqlalchemy.orm import Session

# Configuración de la base de datos
from database import Base, engine, SessionLocal

# Modelos de tablas
from models import Socio
import models

# Esquemas (validación de datos recibidos)
from schemas import SocioCreate


# ============================================================
# CREACIÓN DE TABLAS
# ============================================================
# Si las tablas no existen, SQLAlchemy las crea automáticamente.

Base.metadata.create_all(bind=engine)


# ============================================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================================

app = FastAPI()


# ============================================================
# CONFIGURACIÓN DE CORS
# ============================================================
# Permite que aplicaciones web externas (frontend)
# consuman esta API.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],      # Permitir GET, POST, PUT, DELETE, etc.
    allow_headers=["*"]
)


# ============================================================
# DEPENDENCIA DE BASE DE DATOS
# ============================================================
# Abre una conexión para cada petición y la cierra al finalizar.

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# RUTA PRINCIPAL
# ============================================================
# Se utiliza para verificar que la API está funcionando.

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "club-app-api"
    }


# ============================================================
# CREAR SOCIO
# ============================================================

@app.post("/socios")
def crear_socio(
    socio: SocioCreate,
    db: Session = Depends(get_db)
):

    # Verificar si el DNI ya existe
    socio_existente = (
        db.query(Socio)
        .filter(Socio.dni == socio.dni)
        .first()
    )

    if socio_existente:
        return {
            "error": "El DNI ya existe"
        }

    # Obtener último número de socio
    ultimo_socio = (
        db.query(Socio)
        .order_by(Socio.numero_socio.desc())
        .first()
    )

    numero_socio = (
        ultimo_socio.numero_socio + 1
        if ultimo_socio
        else 1
    )

    # Crear nuevo registro
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


# ============================================================
# LISTAR TODOS LOS SOCIOS
# ============================================================

@app.get("/socios")
def listar_socios(
    db: Session = Depends(get_db)
):
    return db.query(Socio).all()


# ============================================================
# OBTENER UN SOCIO POR NÚMERO
# ============================================================

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


# ============================================================
# MODIFICAR SOCIO
# ============================================================

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

    # Verificar DNI duplicado
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

    # Actualizar datos
    socio.nombre = datos.nombre
    socio.apellido = datos.apellido
    socio.dni = datos.dni
    socio.fecha_nacimiento = datos.fecha_nacimiento

    db.commit()
    db.refresh(socio)

    return {
        "mensaje": "Socio modificado correctamente"
    }


# ============================================================
# ELIMINAR SOCIO
# ============================================================

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
```

