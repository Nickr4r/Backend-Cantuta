from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class AlumnoBase(BaseModel):
    dni: str
    nombres: str
    apellidos: str
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class AlumnoCreate(AlumnoBase):
    pass # Para crear usamos todos los campos base

class AlumnoResponse(AlumnoBase):
    id_alumno: int
    estado: str
    class Config:
        from_attributes = True