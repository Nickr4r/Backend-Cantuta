from pydantic import BaseModel, EmailStr # <--- Cambiado para validar correos
from typing import Optional
from datetime import datetime
from app.core.roles import RoleID

# Esquema base con campos comunes
class UserBase(BaseModel):
    username: str
    id_rol: RoleID

# Esquema para la creación de usuarios (Entrada)
class UserCreate(UserBase):
    password: str
    dni_vinculo: Optional[str] = None 

# Esquema para el Login (Entrada)
class UserLogin(BaseModel):
    username: str
    password: str

# Esquema para la entrega del Token JWT (Salida)
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para las respuestas de la API (Salida)
class UserResponse(UserBase):
    id_usuario: int
    id_docente: Optional[int] = None
    id_alumno: Optional[int] = None
    id_personal: Optional[int] = None
    ultimo_acceso: Optional[datetime] = None
    estado: str
    fecha_creacion: datetime
    
    # Campo de seguridad
    requiere_cambio_pwd: bool 

    # Campos virtuales procesados en el Backend
    dni_vinculado: Optional[str] = None
    nombre_completo: Optional[str] = None

    class Config:
        from_attributes = True

# Esquema para la actualización de usuarios (Entrada)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    id_rol: Optional[RoleID] = None
    estado: Optional[str] = None
    requiere_cambio_pwd: Optional[bool] = None

# --- RECUPERACIÓN DE CONTRASEÑA ---

class PasswordResetRequest(BaseModel):
    # Usar EmailStr obliga a que el usuario mande un formato @valido.com
    username: str
    email: EmailStr 

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str