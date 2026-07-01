from sqlalchemy.orm import Session
from app.domain.models import PersonalAdministrativo

class PersonalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(PersonalAdministrativo).all()

    def get_by_id(self, id_personal: int):
        return self.db.query(PersonalAdministrativo).filter(PersonalAdministrativo.id_personal == id_personal).first()

    def get_by_dni(self, dni: str):
        return self.db.query(PersonalAdministrativo).filter(PersonalAdministrativo.dni == dni).first()

    def create(self, personal_obj: PersonalAdministrativo):
        self.db.add(personal_obj)
        self.db.commit()
        self.db.refresh(personal_obj)
        return personal_obj

    def update(self):
        self.db.commit()