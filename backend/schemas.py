# ============================================================
# IMPORTACIONES
# ============================================================

# BaseModel permite crear esquemas de validación
# para los datos recibidos y enviados por la API.

from pydantic import BaseModel


# ============================================================
# ESQUEMA DE CREACIÓN DE SOCIOS
# ============================================================
# Este esquema define los datos que el backend espera
# recibir cuando se crea o modifica un socio.
#
# FastAPI utiliza esta clase para:
# - Validar datos automáticamente.
# - Generar documentación en /docs.
# - Convertir JSON en objetos Python.

class SocioCreate(BaseModel):

    # Nombre del socio
    nombre: str

    # Apellido del socio
    apellido: str

    # Documento Nacional de Identidad
    dni: str

    # Fecha de nacimiento
    # Formato esperado:
    # YYYY-MM-DD
    fecha_nacimiento: str
