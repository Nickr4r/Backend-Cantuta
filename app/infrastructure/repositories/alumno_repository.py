from sqlalchemy.orm import Session
from app.domain.models import Alumno

class AlumnoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Alumno).offset(skip).limit(limit).all()

    def get_by_dni(self, dni: str):
        return self.db.query(Alumno).filter(Alumno.dni == dni).first()

    def create(self, alumno_obj: Alumno):
        self.db.add(alumno_obj)
        self.db.commit()
        self.db.refresh(alumno_obj)
        return alumno_obj