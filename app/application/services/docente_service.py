from fastapi import HTTPException, status
from app.infrastructure.repositories.docente_repository import DocenteRepository
from app.infrastructure.repositories.alumno_repository import AlumnoRepository
from app.infrastructure.repositories.personal_repository import PersonalRepository
from app.domain.models import Docente
from app.core.roles import RoleID # IMPORTAR PARA VALIDAR PERMISOS

class DocenteService:
    def __init__(self, db):
        self.repo = DocenteRepository(db)
        self.alumno_repo = AlumnoRepository(db)
        self.personal_repo = PersonalRepository(db)

    def listar_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, id_docente: int, current_user):
        # 1. Buscar al docente
        docente = self.repo.get_by_id(id_docente)
        if not docente:
            raise HTTPException(status_code=404, detail="Docente no encontrado")

        # 2. VALIDACIÓN DE SEGURIDAD:
        # Permite acceso si es Admin/Director O si es el mismo Docente logueado.
        es_gestion = current_user.id_rol in [RoleID.DIRECTOR, RoleID.ADMINISTRATIVO]
        es_propietario = current_user.id_docente == id_docente

        if not (es_gestion or es_propietario):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permiso para acceder al perfil de otro docente"
            )

        return docente

    def registrar_docente(self, datos):
        # Validación cruzada de DNI
        if self.repo.get_by_dni(datos.dni) or self.alumno_repo.get_by_dni(datos.dni) or self.personal_repo.get_by_dni(datos.dni):
            raise HTTPException(status_code=400, detail="El DNI ya se encuentra registrado en el sistema")

        nuevo_docente = Docente(**datos.model_dump())
        return self.repo.create(nuevo_docente)

    def actualizar_docente(self, id_docente: int, datos_nuevos):
        docente = self.repo.get_by_id(id_docente)
        if not docente: raise HTTPException(404, "Docente no encontrado")
        
        data = datos_nuevos.model_dump(exclude_unset=True)

        # Si cambia el DNI, validación cruzada
        if "dni" in data and data["dni"] != docente.dni:
            if self.repo.get_by_dni(data["dni"]) or self.alumno_repo.get_by_dni(data["dni"]) or self.personal_repo.get_by_dni(data["dni"]):
                raise HTTPException(status_code=400, detail="El nuevo DNI ya está ocupado")

        for key, value in data.items():
            setattr(docente, key, value)
            
        self.repo.update()
        return docente

    def eliminar_docente(self, id_docente: int):
        docente = self.repo.get_by_id(id_docente)
        if not docente: raise HTTPException(404, "Docente no encontrado")
        docente.estado = "inactivo"
        self.repo.update()
        return {"message": "Docente dado de baja correctamente"}