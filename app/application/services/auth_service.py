# app/application/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.alumno_repository import AlumnoRepository
from app.infrastructure.repositories.docente_repository import DocenteRepository
from app.infrastructure.repositories.personal_repository import PersonalRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.domain.models import Usuario
from app.core.roles import RoleID

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.alumno_repo = AlumnoRepository(db)
        self.docente_repo = DocenteRepository(db)
        self.personal_repo = PersonalRepository(db)

    def register_user(self, user_data):
        # 1. Validación de seguridad: ¿El nombre de usuario ya existe?
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El nombre de usuario ya está en uso"
            )

        # 2. Preparar los campos de vinculación
        id_alumno = None
        id_docente = None
        id_personal = None

        # 3. Lógica de Vinculación por Rol (Blindada)
        
        # CASO ESTUDIANTE: Busca obligatoriamente en Alumnos
        if user_data.id_rol == RoleID.ESTUDIANTE:
            if not user_data.dni_vinculo:
                raise HTTPException(status_code=400, detail="Se requiere DNI para vincular al Estudiante")
            
            persona = self.alumno_repo.get_by_dni(user_data.dni_vinculo)
            if not persona:
                raise HTTPException(status_code=404, detail="DNI no encontrado en el registro de ALUMNOS")
            id_alumno = persona.id_alumno

        # CASO DOCENTE: Busca obligatoriamente en Docentes
        elif user_data.id_rol == RoleID.DOCENTE:
            if not user_data.dni_vinculo:
                raise HTTPException(status_code=400, detail="Se requiere DNI para vincular al Docente")
            
            persona = self.docente_repo.get_by_dni(user_data.dni_vinculo)
            if not persona:
                raise HTTPException(status_code=404, detail="DNI no encontrado en el registro de DOCENTES")
            id_docente = persona.id_docente

        # CASO GESTIÓN: Busca en Personal Administrativo
        elif user_user_data.id_rol in [RoleID.DIRECTOR, RoleID.ADMINISTRATIVO]:
            if user_data.dni_vinculo: # El vínculo es opcional para el Director en el código, pero si viene se valida
                persona = self.personal_repo.get_by_dni(user_data.dni_vinculo)
                if not persona:
                    raise HTTPException(status_code=404, detail="DNI no encontrado en PERSONAL ADMINISTRATIVO")
                id_personal = persona.id_personal

        # 4. Encriptación y Creación
        hashed_pwd = get_password_hash(user_data.password)
        
        nuevo_usuario = Usuario(
            username=user_data.username,
            password_hash=hashed_pwd,
            id_rol=user_data.id_rol,
            id_alumno=id_alumno,
            id_docente=id_docente,
            id_personal=id_personal,
            estado="activo"
        )
        
        return self.user_repo.create(nuevo_usuario)

    def authenticate(self, username, password):
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        
        # Incluimos el rol en el token para que el frontend sepa qué menús mostrar
        token_data = {
            "sub": user.username,
            "rol": user.id_rol
        }
        return create_access_token(data=token_data)