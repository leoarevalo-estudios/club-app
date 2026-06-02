from pydantic import BaseModel


class SocioCreate(BaseModel):
    nombre: str
    apellido: str
    dni: str
    fecha_nacimiento: str