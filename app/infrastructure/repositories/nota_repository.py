from sqlalchemy.orm import Session
from app.domain.models import Nota

class NotaRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_nota(self, nota_obj: Nota):
        self.db.add(nota_obj)
        self.db.commit()
        self.db.refresh(nota_obj)
        return nota_obj

    def get_notas_by_matricula(self, id_matricula: int):
        return self.db.query(Nota).filter(Nota.id_matricula == id_matricula).all()