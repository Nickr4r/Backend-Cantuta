from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.domain.models import Usuario

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, user_data):
        # 1. Hashear la contraseña
        hashed_pwd = get_password_hash(user_data.password)
        
        # 2. Crear objeto del dominio
        new_user = Usuario(
            username=user_data.username,
            password_hash=hashed_pwd,
            id_rol=user_data.id_rol,
            id_docente=user_data.id_docente,
            id_alumno=user_data.id_alumno
        )
        
        # 3. Guardar usando el repositorio
        return self.user_repo.create(new_user)

    def authenticate(self, username, password):
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        
        # Generar token si todo está bien
        token = create_access_token(data={"sub": user.username, "rol": user.id_rol})
        return token