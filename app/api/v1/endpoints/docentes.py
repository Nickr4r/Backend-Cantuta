from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.api.schemas.docente_schema import DocenteCreate, DocenteResponse
from app.application.services.docente_service import DocenteService
from app.api.v1.dependencies import admin_required

router = APIRouter()

@router.post("/", response_model=DocenteResponse, status_code=status.HTTP_201_CREATED)
def crear_docente(
    datos: DocenteCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    servicio = DocenteService(db)
    return servicio.registrar_docente(datos)