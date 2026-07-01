from fastapi import HTTPException
from app.infrastructure.repositories.docente_repository import DocenteRepository
from app.domain.models import Docente

class DocenteService:
    def __init__(self, db):
        self.repo = DocenteRepository(db)

    def listar_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, id_docente: int):
        docente = self.repo.get_by_id(id_docente)
        if not docente:
            raise HTTPException(status_code=404, detail="Docente no encontrado")
        return docente

    def registrar_docente(self, datos):
        if self.repo.get_by_dni(datos.dni):
            raise HTTPException(status_code=400, detail="El DNI del docente ya existe")
        nuevo_docente = Docente(**datos.model_dump())
        return self.repo.create(nuevo_docente)

    def actualizar_docente(self, id_docente: int, datos_nuevos):
        docente = self.obtener_por_id(id_docente)
        for key, value in datos_nuevos.model_dump(exclude_unset=True).items():
            setattr(docente, key, value)
        self.repo.update()
        return docente

    def eliminar_docente(self, id_docente: int):
        docente = self.obtener_por_id(id_docente)
        docente.estado = "inactivo"
        self.repo.update()
        return {"message": "Docente dado de baja correctamente"}