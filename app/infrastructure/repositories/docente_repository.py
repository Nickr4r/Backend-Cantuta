from sqlalchemy.orm import Session
from app.domain.models import Docente

class DocenteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_dni(self, dni: str):
        return self.db.query(Docente).filter(Docente.dni == dni).first()

    def create(self, docente_obj: Docente):
        self.db.add(docente_obj)
        self.db.commit()
        self.db.refresh(docente_obj)
        return docente_obj

    def get_all(self):
        return self.db.query(Docente).all()