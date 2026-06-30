from sqlalchemy.orm import Session
from app.domain.models import Usuario

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def create(self, user_obj: Usuario):
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj

    def update_last_login(self, user_id: int):
        from datetime import datetime
        user = self.get_by_id(user_id)
        if user:
            user.ultimo_acceso = datetime.now()
            self.db.commit()