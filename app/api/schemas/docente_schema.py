from pydantic import BaseModel, EmailStr
from typing import Optional

class DocenteBase(BaseModel):
    dni: str
    nombres: str
    apellidos: str
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class DocenteCreate(DocenteBase):
    pass # Datos necesarios para la creación

class DocenteResponse(DocenteBase):
    id_docente: int
    estado: str

    class Config:
        from_attributes = True