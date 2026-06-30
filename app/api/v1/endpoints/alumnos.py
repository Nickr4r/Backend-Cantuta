from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.api.schemas.alumno_schema import AlumnoCreate, AlumnoResponse
from app.application.services.alumno_service import AlumnoService
from app.api.v1.dependencies import admin_required # Tu candado de seguridad

router = APIRouter()

@router.post("/", response_model=AlumnoResponse, status_code=status.HTTP_201_CREATED)
def crear_alumno(
    datos: AlumnoCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(admin_required) # Solo Director o Administrativo
):
    servicio = AlumnoService(db)
    return servicio.registrar_alumno(datos)