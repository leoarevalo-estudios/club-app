
# ============================================================
# IMPORTACIONES
# ============================================================

# Tipos de columnas disponibles en SQLAlchemy
from sqlalchemy import Column, Integer, String

# Clase base de la que heredarán todos los modelos
from database import Base


# ============================================================
# MODELO SOCIO
# ============================================================
# Esta clase representa la tabla "socios" dentro
# de la base de datos.
#
# Cada atributo de la clase corresponde a una columna
# de la tabla.

class Socio(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "socios"


    # ========================================================
    # CLAVE PRIMARIA
    # ========================================================
    # Identificador interno único generado automáticamente.
    #
    # No se utiliza como número de socio visible para el usuario.
    # Su función principal es identificar cada registro dentro
    # de la base de datos.

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # ========================================================
    # NÚMERO DE SOCIO
    # ========================================================
    # Número visible para el usuario.
    # Debe ser único y obligatorio.

    numero_socio = Column(
        Integer,
        unique=True,
        nullable=False
    )


    # ========================================================
    # NOMBRE
    # ========================================================
    # Nombre del socio.
    # Campo obligatorio.

    nombre = Column(
        String,
        nullable=False
    )


    # ========================================================
    # APELLIDO
    # ========================================================
    # Apellido del socio.
    # Campo obligatorio.

    apellido = Column(
        String,
        nullable=False
    )


    # ========================================================
    # DNI
    # ========================================================
    # Documento Nacional de Identidad.
    #
    # Debe ser único para evitar registros duplicados.

    dni = Column(
        String,
        unique=True,
        nullable=False
    )


    # ========================================================
    # FECHA DE NACIMIENTO
    # ========================================================
    # Fecha de nacimiento almacenada como texto.
    #
    # Ejemplo:
    # 2001-02-02

    fecha_nacimiento = Column(
        String,
        nullable=False
    )
