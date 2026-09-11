from sqlalchemy.orm import Session
from sqlalchemy import or_  # IMPORTANTE: Para buscar en varias tablas
from app.domain.models import Usuario, Alumno, Docente, PersonalAdministrativo

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def get_all(self):
        return self.db.query(Usuario).all()

    def get_paginated(self, skip: int = 0, limit: int = 10, search: str = None):
        """
        Busca usuarios, docentes, alumnos o personal administrativo
        haciendo joins con sus tablas respectivas.
        """
        # Hacemos los JOINs hacia afuera para no perder usuarios que no tengan vínculo
        query = self.db.query(Usuario).outerjoin(Alumno).outerjoin(Docente).outerjoin(PersonalAdministrativo)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Usuario.username.ilike(search_filter),
                    Alumno.dni.ilike(search_filter),
                    Alumno.nombres.ilike(search_filter),
                    Alumno.apellidos.ilike(search_filter),
                    Docente.dni.ilike(search_filter),
                    Docente.nombres.ilike(search_filter),
                    Docente.apellidos.ilike(search_filter),
                    PersonalAdministrativo.dni.ilike(search_filter),
                    PersonalAdministrativo.nombres.ilike(search_filter),
                    PersonalAdministrativo.apellidos.ilike(search_filter)
                )
            )
            
        return query.order_by(Usuario.fecha_creacion.desc()).offset(skip).limit(limit).all()

    def count_all(self, search: str = None):
        query = self.db.query(Usuario).outerjoin(Alumno).outerjoin(Docente).outerjoin(PersonalAdministrativo)
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Usuario.username.ilike(search_filter),
                    Alumno.dni.ilike(search_filter),
                    Alumno.nombres.ilike(search_filter),
                    Alumno.apellidos.ilike(search_filter),
                    Docente.dni.ilike(search_filter),
                    Docente.nombres.ilike(search_filter),
                    Docente.apellidos.ilike(search_filter),
                    PersonalAdministrativo.dni.ilike(search_filter),
                    PersonalAdministrativo.nombres.ilike(search_filter),
                    PersonalAdministrativo.apellidos.ilike(search_filter)
                )
            )
        return query.count()

    def create(self, user_obj: Usuario):
        self.db.add(user_obj)
        self.save()
        self.db.refresh(user_obj)
        return user_obj

    def save(self):
        self.db.commit()