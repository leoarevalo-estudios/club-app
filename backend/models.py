from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Socio(Base):
    __tablename__ = "socios"

    id = Column(Integer, primary_key=True, index=True)

    numero_socio = Column(
        Integer,
        unique=True,
        nullable=False
    )

    nombre = Column(
        String,
        nullable=False
    )

    apellido = Column(
        String,
        nullable=False
    )

    dni = Column(
        String,
        unique=True,
        nullable=False
    )

    fecha_nacimiento = Column(
        String,
        nullable=False
    )