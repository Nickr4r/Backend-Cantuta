from sqlalchemy.orm import Session
from app.infrastructure.repositories.docente_repository import DocenteRepository
from app.domain.models import Docente
from fastapi import HTTPException

class DocenteService:
    def __init__(self, db: Session):
        self.docente_repo = DocenteRepository(db)

    def registrar_docente(self, docente_data):
        # Regla de negocio: DNI único
        db_docente = self.docente_repo.get_by_dni(docente_data.dni)
        if db_docente:
            raise HTTPException(status_code=400, detail="El DNI del docente ya está registrado")
        
        # Mapeo de Schema a Modelo de Dominio
        nuevo_docente = Docente(**docente_data.model_dump())
        return self.docente_repo.create(nuevo_docente)