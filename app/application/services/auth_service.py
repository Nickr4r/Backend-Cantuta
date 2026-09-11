# app/application/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt, JWTError

# Repositorios
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.alumno_repository import AlumnoRepository
from app.infrastructure.repositories.docente_repository import DocenteRepository
from app.infrastructure.repositories.personal_repository import PersonalRepository

# Seguridad, Correo y Dominio
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_password_reset_token,
    SECRET_KEY, 
    ALGORITHM
)
from app.core.mail import enviar_correo_recuperacion
from app.domain.models import Usuario
from app.core.roles import RoleID
from app.api.schemas.user_schema import UserUpdate

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.alumno_repo = AlumnoRepository(db)
        self.docente_repo = DocenteRepository(db)
        self.personal_repo = PersonalRepository(db)

    def register_user(self, user_data):
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

        id_alumno, id_docente, id_personal = None, None, None

        if user_data.id_rol == RoleID.ESTUDIANTE:
            if not user_data.dni_vinculo:
                raise HTTPException(status_code=400, detail="DNI requerido para Estudiante")
            p = self.alumno_repo.get_by_dni(user_data.dni_vinculo)
            if not p: raise HTTPException(status_code=404, detail="Alumno no encontrado")
            if p.usuario: raise HTTPException(status_code=400, detail="Este alumno ya tiene usuario")
            id_alumno = p.id_alumno

        elif user_data.id_rol == RoleID.DOCENTE:
            if not user_data.dni_vinculo:
                raise HTTPException(status_code=400, detail="DNI requerido para Docente")
            p = self.docente_repo.get_by_dni(user_data.dni_vinculo)
            if not p: raise HTTPException(status_code=404, detail="Docente no encontrado")
            if p.usuario: raise HTTPException(status_code=400, detail="Este docente ya tiene usuario")
            id_docente = p.id_docente

        elif user_data.id_rol in [RoleID.DIRECTOR, RoleID.ADMINISTRATIVO]:
            if user_data.dni_vinculo:
                p = self.personal_repo.get_by_dni(user_data.dni_vinculo)
                if not p: raise HTTPException(status_code=404, detail="Personal no encontrado")
                if p.usuario: raise HTTPException(status_code=400, detail="Este personal ya tiene usuario")
                id_personal = p.id_personal

        nuevo_usuario = Usuario(
            username=user_data.username,
            password_hash=get_password_hash(user_data.password),
            id_rol=user_data.id_rol,
            id_alumno=id_alumno,
            id_docente=id_docente,
            id_personal=id_personal,
            estado="activo",
            requiere_cambio_pwd=True
        )
        return self.user_repo.create(nuevo_usuario)

    def authenticate(self, username, password):
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash) or user.estado != "activo":
            return None
            
        token_data = {
            "sub": user.username,
            "rol": user.id_rol,
            "id_usuario": user.id_usuario,
            "id_alumno": user.id_alumno,
            "id_docente": user.id_docente,
            "id_personal": user.id_personal,
            "requiere_cambio_pwd": user.requiere_cambio_pwd
        }
        return create_access_token(data=token_data)

    def listar_usuarios(self, skip: int = 0, limit: int = 10, search: str = None):
        """Ahora incluye paginación y búsqueda"""
        return self.user_repo.get_paginated(skip=skip, limit=limit, search=search)

    def actualizar_usuario(self, user_id: int, datos_nuevos: UserUpdate, current_user):
        user_to_edit = self.user_repo.get_by_id(user_id)
        if not user_to_edit: 
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        es_admin = current_user.id_rol in [RoleID.DIRECTOR, RoleID.ADMINISTRATIVO]
        es_el_mismo = current_user.id_usuario == user_id

        if not (es_admin or es_el_mismo):
            raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta cuenta")

        data = datos_nuevos.model_dump(exclude_unset=True)
        
        if "username" in data:
            existente = self.user_repo.get_by_username(data["username"])
            if existente and existente.id_usuario != user_id:
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está ocupado")

        if "password" in data:
            user_to_edit.password_hash = get_password_hash(data["password"])
            user_to_edit.requiere_cambio_pwd = False 
            del data["password"]

        for key, value in data.items():
            setattr(user_to_edit, key, value)

        self.user_repo.save()
        return user_to_edit

    async def solicitar_restablecimiento(self, username: str, email: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        email_valido = False
        if user.alumno and user.alumno.correo == email:
            email_valido = True
        elif user.docente and user.docente.correo == email:
            email_valido = True
        elif user.personal and user.personal.correo == email:
            email_valido = True

        if not email_valido:
            raise HTTPException(status_code=400, detail="El correo no coincide con la cuenta")

        token_reset = create_password_reset_token(user.id_usuario)

        try:
            await enviar_correo_recuperacion(email, token_reset)
            return {"message": "Enlace enviado exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error enviando correo")

    def confirmar_restablecimiento(self, token: str, nueva_password: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("scope") != "password_reset":
                raise HTTPException(status_code=400, detail="Token no válido")
                
            user = self.user_repo.get_by_id(payload.get("user_id"))
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            user.password_hash = get_password_hash(nueva_password)
            user.requiere_cambio_pwd = False
            self.user_repo.save()
            return {"message": "Contraseña actualizada exitosamente"}
        except JWTError:
            raise HTTPException(status_code=400, detail="Token inválido o expirado")