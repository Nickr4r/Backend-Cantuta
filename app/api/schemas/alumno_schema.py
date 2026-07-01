# app/api/schemas/alumno_schema.py
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
    pass

class AlumnoResponse(AlumnoBase):
    id_alumno: int
    estado: str
    class Config:
        from_attributes = True

class AlumnoUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[str] = None