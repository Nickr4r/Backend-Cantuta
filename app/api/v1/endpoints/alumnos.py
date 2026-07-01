from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.api.schemas.alumno_schema import AlumnoCreate, AlumnoResponse, AlumnoUpdate
from app.application.services.alumno_service import AlumnoService
from app.api.v1.dependencies import admin_required
from typing import List

router = APIRouter()

@router.get("/", response_model=List[AlumnoResponse], summary="Listar todos los alumnos")
def listar(db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return AlumnoService(db).listar_todos()

@router.get("/{id_alumno}", response_model=AlumnoResponse, summary="Obtener un alumno por ID")
def obtener(id_alumno: int, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return AlumnoService(db).obtener_por_id(id_alumno)

@router.post("/", response_model=AlumnoResponse, status_code=status.HTTP_201_CREATED, summary="Registrar alumno")
def crear(datos: AlumnoCreate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return AlumnoService(db).registrar_alumno(datos)

@router.patch("/{id_alumno}", response_model=AlumnoResponse, summary="Actualizar datos de un alumno")
def actualizar(id_alumno: int, datos: AlumnoUpdate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return AlumnoService(db).actualizar_alumno(id_alumno, datos)

@router.delete("/{id_alumno}", summary="Dar de baja a un alumno")
def eliminar(id_alumno: int, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return AlumnoService(db).eliminar_alumno(id_alumno)