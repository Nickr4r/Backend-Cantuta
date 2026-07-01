from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.api.schemas.docente_schema import DocenteCreate, DocenteResponse, DocenteUpdate
from app.application.services.docente_service import DocenteService
from app.api.v1.dependencies import admin_required
from typing import List

router = APIRouter()

@router.get("/", response_model=List[DocenteResponse], summary="Listar todos los docentes")
def listar(db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return DocenteService(db).listar_todos()

@router.get("/{id_docente}", response_model=DocenteResponse, summary="Obtener un docente por ID")
def obtener(id_docente: int, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return DocenteService(db).obtener_por_id(id_docente)

@router.post("/", response_model=DocenteResponse, status_code=status.HTTP_201_CREATED, summary="Registrar nuevo docente")
def crear(datos: DocenteCreate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return DocenteService(db).registrar_docente(datos)

@router.patch("/{id_docente}", response_model=DocenteResponse, summary="Actualizar datos de un docente")
def actualizar(id_docente: int, datos: DocenteUpdate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return DocenteService(db).actualizar_docente(id_docente, datos)

@router.delete("/{id_docente}", summary="Dar de baja a un docente")
def eliminar(id_docente: int, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return DocenteService(db).eliminar_docente(id_docente)