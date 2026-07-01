from pydantic import BaseModel, EmailStr
from typing import Optional

class PersonalBase(BaseModel):
    dni: str
    nombres: str
    apellidos: str
    cargo: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class PersonalCreate(PersonalBase):
    pass

class PersonalResponse(PersonalBase):
    id_personal: int
    estado: str
    class Config:
        from_attributes = True

class PersonalUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    cargo: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[str] = None