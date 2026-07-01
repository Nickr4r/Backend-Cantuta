from fastapi import HTTPException
from app.infrastructure.repositories.alumno_repository import AlumnoRepository
from app.domain.models import Alumno

class AlumnoService:
    def __init__(self, db):
        self.repo = AlumnoRepository(db)

    def listar_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, id_alumno: int):
        alumno = self.repo.get_by_id(id_alumno)
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return alumno

    def registrar_alumno(self, datos):
        if self.repo.get_by_dni(datos.dni):
            raise HTTPException(status_code=400, detail="DNI ya registrado")
        nuevo_alumno = Alumno(**datos.model_dump())
        return self.repo.create(nuevo_alumno)

    def actualizar_alumno(self, id_alumno: int, datos_nuevos):
        alumno = self.obtener_por_id(id_alumno)
        for key, value in datos_nuevos.model_dump(exclude_unset=True).items():
            setattr(alumno, key, value)
        self.repo.update()
        return alumno

    def eliminar_alumno(self, id_alumno: int):
        alumno = self.obtener_por_id(id_alumno)
        alumno.estado = "inactivo" # Borrado lógico
        self.repo.update()
        return {"message": "Alumno dado de baja correctamente"}