# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.api.schemas.user_schema import UserCreate, UserLogin, Token
from app.application.services.auth_service import AuthService
from app.api.v1.dependencies import admin_required

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_admin = Depends(admin_required)
):
    """
    Crea un nuevo usuario. 
    Requiere un token de Administrador o Director.
    """
    auth_service = AuthService(db)
    existing_user = auth_service.user_repo.get_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        
    return auth_service.register_user(user)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Inicia sesión y devuelve un Token JWT.
    Este endpoint es público.
    """
    auth_service = AuthService(db)
    token = auth_service.authenticate(credentials.username, credentials.password)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario o contraseña incorrectos"
        )
    
    return {"access_token": token, "token_type": "bearer"}