from sqlalchemy.orm import Session
from app.infrastructure.repositories.alumno_repository import AlumnoRepository
from app.domain.models import Alumno
from fastapi import HTTPException

class AlumnoService:
    def __init__(self, db: Session):
        self.alumno_repo = AlumnoRepository(db)

    def registrar_alumno(self, datos_alumno):
        # Regla: No pueden haber dos alumnos con el mismo DNI
        existente = self.alumno_repo.get_by_dni(datos_alumno.dni)
        if existente:
            raise HTTPException(status_code=400, detail="El DNI ya pertenece a otro alumno")
        
        # Convertimos el Schema a Modelo de DB
        nuevo_alumno = Alumno(**datos_alumno.model_dump())
        return self.alumno_repo.create(nuevo_alumno)