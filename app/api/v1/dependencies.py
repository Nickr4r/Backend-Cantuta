# app/api/v1/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.roles import RoleID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token no contiene el usuario"
            )
            
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Sesión expirada o token inválido"
        )
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(username)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="El usuario del token ya no existe"
        )
    return user

def admin_required(current_user = Depends(get_current_user)):
    # USAMOS LOS ROLES DEFINIDOS EN EL ENUM
    if current_user.id_rol not in [RoleID.DIRECTOR, RoleID.ADMINISTRATIVO]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acceso denegado: Se requiere rol de Director o Administrativo"
        )
    return current_user