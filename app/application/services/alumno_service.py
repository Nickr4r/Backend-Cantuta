from fastapi import HTTPException, status
from app.infrastructure.repositories.alumno_repository import AlumnoRepository
from app.infrastructure.repositories.docente_repository import DocenteRepository
from app.infrastructure.repositories.personal_repository import PersonalRepository
from app.domain.models import Alumno
from app.core.roles import RoleID # IMPORTAR PARA VALIDAR ROLES

class AlumnoService:
    def __init__(self, db):
        self.repo = AlumnoRepository(db)
        self.docente_repo = DocenteRepository(db)
        self.personal_repo = PersonalRepository(db)

    def listar_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, id_alumno: int, current_user):
        # 1. Buscamos el registro
        alumno = self.repo.get_by_id(id_alumno)
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")

        # 2. VALIDACIÓN DE PERMISOS:
        # El acceso se permite si el usuario es Admin/Director 
        # O si el id_alumno del token coincide con el que están pidiendo.
        es_gestion = current_user.id_rol in [RoleID.DIRECTOR, RoleID.ADMINISTRATIVO]
        es_propietario = current_user.id_alumno == id_alumno

        if not (es_gestion or es_propietario):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permiso para ver datos de otro usuario"
            )

        return alumno

    def registrar_alumno(self, datos):
        if self.repo.get_by_dni(datos.dni) or self.docente_repo.get_by_dni(datos.dni) or self.personal_repo.get_by_dni(datos.dni):
            raise HTTPException(status_code=400, detail="El DNI ya existe en el sistema")
        
        nuevo_alumno = Alumno(**datos.model_dump())
        return self.repo.create(nuevo_alumno)

    def actualizar_alumno(self, id_alumno: int, datos_nuevos):
        # Aquí también podrías usar el current_user si quieres que el alumno edite su propia info
        alumno = self.repo.get_by_id(id_alumno) 
        if not alumno: raise HTTPException(404, "Alumno no encontrado")

        data = datos_nuevos.model_dump(exclude_unset=True)
        # Validar DNI nuevo si cambió (validación cruzada)
        if "dni" in data and data["dni"] != alumno.dni:
             if self.repo.get_by_dni(data["dni"]) or self.docente_repo.get_by_dni(data["dni"]) or self.personal_repo.get_by_dni(data["dni"]):
                raise HTTPException(status_code=400, detail="El nuevo DNI ya está ocupado")

        for key, value in data.items():
            setattr(alumno, key, value)
            
        self.repo.update()
        return alumno

    def eliminar_alumno(self, id_alumno: int):
        alumno = self.repo.get_by_id(id_alumno)
        if not alumno: raise HTTPException(404, "Alumno no encontrado")
        alumno.estado = "inactivo"
        self.repo.update()
        return {"message": "Alumno dado de baja correctamente"}