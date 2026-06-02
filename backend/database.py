# ============================================================
# IMPORTACIONES
# ============================================================

# Crea la conexión con la base de datos
from sqlalchemy import create_engine

# Clase base para todos los modelos de SQLAlchemy
from sqlalchemy.orm import declarative_base

# Generador de sesiones para interactuar con la base de datos
from sqlalchemy.orm import sessionmaker


# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================
# URL de conexión.
#
# sqlite:///./club.db
#
# Significa:
# - sqlite://  -> Motor SQLite
# - ./club.db  -> Archivo club.db ubicado en la carpeta actual

DATABASE_URL = "sqlite:///./club.db"


# ============================================================
# MOTOR DE BASE DE DATOS (ENGINE)
# ============================================================
# El engine es la conexión principal entre la aplicación
# y la base de datos.
#
# connect_args={"check_same_thread": False}
#
# SQLite normalmente limita el acceso a un único hilo.
# FastAPI puede manejar múltiples peticiones simultáneas,
# por lo que esta configuración evita errores de conexión.

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# ============================================================
# FÁBRICA DE SESIONES
# ============================================================
# SessionLocal genera nuevas sesiones de trabajo.
#
# Cada petición de la API abre una sesión,
# realiza consultas o modificaciones,
# y luego la cierra.
#
# autocommit=False
#   Los cambios no se guardan automáticamente.
#
# autoflush=False
#   SQLAlchemy no sincroniza automáticamente
#   los cambios pendientes con la base de datos.
#
# bind=engine
#   Vincula las sesiones al motor configurado.

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# CLASE BASE DE LOS MODELOS
# ============================================================
# Todos los modelos heredarán de esta clase.
#
# Ejemplo:
#
# class Socio(Base):
#     __tablename__ = "socios"
#
# SQLAlchemy utiliza esta clase para conocer
# todas las tablas del proyecto.

Base = declarative_base()

