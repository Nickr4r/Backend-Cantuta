from fastapi import HTTPException, status
from app.infrastructure.repositories.personal_repository import PersonalRepository
from app.infrastructure.repositories.alumno_repository import AlumnoRepository
from app.infrastructure.repositories.docente_repository import DocenteRepository
from app.domain.models import PersonalAdministrativo
from app.core.roles import RoleID # IMPORTAR

class PersonalService:
    def __init__(self, db):
        self.repo = PersonalRepository(db)
        self.alumno_repo = AlumnoRepository(db)
        self.docente_repo = DocenteRepository(db)

    def listar_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, id_personal: int, current_user):
        # 1. Buscar el registro
        personal = self.repo.get_by_id(id_personal)
        if not personal:
            raise HTTPException(status_code=404, detail="Personal no encontrado")

        # 2. VALIDACIÓN DE SEGURIDAD:
        # Permite si es Admin/Director O si es el dueño de la cuenta (id_personal coincide)
        es_gestion = current_user.id_rol in [RoleID.DIRECTOR, RoleID.ADMINISTRATIVO]
        es_propietario = current_user.id_personal == id_personal

        if not (es_gestion or es_propietario):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permiso para ver los datos de otra persona"
            )

        return personal

    def registrar_personal(self, datos):
        # Validación cruzada de DNI
        if self.repo.get_by_dni(datos.dni) or self.alumno_repo.get_by_dni(datos.dni) or self.docente_repo.get_by_dni(datos.dni):
            raise HTTPException(status_code=400, detail="Este DNI ya está registrado en el sistema")

        nuevo = PersonalAdministrativo(**datos.model_dump())
        return self.repo.create(nuevo)

    def actualizar_personal(self, id_personal: int, datos_nuevos):
        personal = self.repo.get_by_id(id_personal)
        if not personal: raise HTTPException(404, "Personal no encontrado")
        
        data = datos_nuevos.model_dump(exclude_unset=True)

        if "dni" in data and data["dni"] != personal.dni:
            if self.repo.get_by_dni(data["dni"]) or self.alumno_repo.get_by_dni(data["dni"]) or self.docente_repo.get_by_dni(data["dni"]):
                raise HTTPException(status_code=400, detail="El nuevo DNI ya está ocupado")

        for key, value in data.items():
            setattr(personal, key, value)
            
        self.repo.update()
        return personal
    
    def eliminar_personal(self, id_personal: int):
        personal = self.repo.get_by_id(id_personal)
        if not personal: raise HTTPException(404, "Personal no encontrado")
        personal.estado = "inactivo" 
        self.repo.update()
        return {"message": "Personal dado de baja correctamente"}