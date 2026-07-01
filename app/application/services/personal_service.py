from fastapi import HTTPException
from app.infrastructure.repositories.personal_repository import PersonalRepository
from app.domain.models import PersonalAdministrativo

class PersonalService:
    def __init__(self, db):
        self.repo = PersonalRepository(db)

    def listar_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, id_personal: int):
        personal = self.repo.get_by_id(id_personal)
        if not personal:
            raise HTTPException(status_code=404, detail="Personal no encontrado")
        return personal

    def registrar_personal(self, datos):
        if self.repo.get_by_dni(datos.dni):
            raise HTTPException(status_code=400, detail="El DNI ya existe")
        nuevo = PersonalAdministrativo(**datos.model_dump())
        return self.repo.create(nuevo)

    def actualizar_personal(self, id_personal: int, datos_nuevos):
        personal = self.obtener_por_id(id_personal)
        for key, value in datos_nuevos.model_dump(exclude_unset=True).items():
            setattr(personal, key, value)
        self.repo.update()
        return personal
    
    def eliminar_personal(self, id_personal: int):
        personal = self.obtener_por_id(id_personal)
        personal.estado = "inactivo" # Borrado lógico para no perder historial
        self.repo.update()
        return {"message": "Personal dado de baja correctamente"}