# app/api/v1/endpoints/auth.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.api.schemas.user_schema import (
    UserCreate, 
    UserLogin, 
    Token, 
    UserResponse, 
    UserUpdate, 
    PasswordResetRequest, 
    PasswordResetConfirm
)
from app.application.services.auth_service import AuthService
from app.api.v1.dependencies import admin_required, get_current_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Inicia sesión y devuelve un JWT con los IDs de vinculación"""
    auth_service = AuthService(db)
    token = auth_service.authenticate(credentials.username, credentials.password)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db), _ = Depends(admin_required)):
    """Solo Director o Administrativo pueden crear usuarios"""
    return AuthService(db).register_user(user)

@router.get("/", response_model=List[UserResponse], summary="Listar usuarios paginados y filtrados")
def listar(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db), 
    _ = Depends(admin_required)
):
    """Solo personal de gestión puede ver la lista de todos los usuarios (Paginado)"""
    return AuthService(db).listar_usuarios(skip=skip, limit=limit, search=search)

@router.patch("/{user_id}", response_model=UserResponse)
def actualizar(
    user_id: int, 
    datos: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user) 
):
    """
    Permite que un ADMIN edite a cualquiera, 
    o que un ALUMNO/DOCENTE se edite a sí mismo.
    """
    auth_service = AuthService(db)
    return auth_service.actualizar_usuario(user_id, datos, current_user)

# --- RUTAS DE RECUPERACIÓN DE CONTRASEÑA ---

@router.post("/recuperar-password")
async def solicitar_recuperacion(datos: PasswordResetRequest, db: Session = Depends(get_db)):
    """Busca el correo y envía un email real."""
    auth_service = AuthService(db)
    return await auth_service.solicitar_restablecimiento(datos.username, datos.email)

@router.post("/restablecer-password")
def confirmar_recuperacion(datos: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Valida el token enviado por correo y actualiza la contraseña en la DB."""
    auth_service = AuthService(db)
    return auth_service.confirmar_restablecimiento(datos.token, datos.new_password)