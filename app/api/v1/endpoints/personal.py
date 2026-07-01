from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.api.schemas.personal_schema import PersonalCreate, PersonalResponse, PersonalUpdate
from app.application.services.personal_service import PersonalService
from app.api.v1.dependencies import admin_required
from typing import List

router = APIRouter()

@router.get("/", response_model=List[PersonalResponse], summary="Listar todo el personal")
def listar(db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return PersonalService(db).listar_todos()

@router.post("/", response_model=PersonalResponse, status_code=status.HTTP_201_CREATED, summary="Registrar personal")
def crear(datos: PersonalCreate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return PersonalService(db).registrar_personal(datos)

@router.patch("/{id_personal}", response_model=PersonalResponse, summary="Actualizar personal")
def actualizar(id_personal: int, datos: PersonalUpdate, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return PersonalService(db).actualizar_personal(id_personal, datos)

@router.get("/{id_personal}", response_model=PersonalResponse, summary="Obtener personal por ID")
def obtener(id_personal: int, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return PersonalService(db).obtener_por_id(id_personal)

@router.delete("/{id_personal}", summary="Dar de baja a personal")
def eliminar(id_personal: int, db: Session = Depends(get_db), current_user = Depends(admin_required)):
    return PersonalService(db).eliminar_personal(id_personal)