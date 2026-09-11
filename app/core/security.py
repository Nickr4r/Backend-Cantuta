# app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os

# Configuración para encriptar contraseñas
# Agregué bcrypt__ident="2b" para evitar conflictos con versiones nuevas de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

SECRET_KEY = os.getenv("SECRET_KEY", "una_clave_secreta_muy_larga_y_segura")
ALGORITHM = "HS256"

# AHORA DURA 24 HORAS (1440 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_password_reset_token(user_id: int):
    """Genera un token JWT que dura 24 horas para recuperar clave"""
    # Cambiado a 24 horas
    expire = datetime.utcnow() + timedelta(hours=24) 
    to_encode = {
        "exp": expire, 
        "user_id": user_id, 
        "scope": "password_reset" 
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)