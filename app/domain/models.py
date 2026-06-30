from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP, Date, Text, DECIMAL, func, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class Role(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text)
    estado = Column(Enum('activo', 'inactivo'), default='activo')

    usuarios = relationship("Usuario", back_populates="rol")


class Alumno(Base):
    __tablename__ = "alumnos"
    id_alumno = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(15), unique=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date)
    sexo = Column(Enum('M', 'F'))
    direccion = Column(String(255))
    telefono = Column(String(20))
    correo = Column(String(100))
    estado = Column(Enum('activo', 'inactivo'), default='activo')

    usuario = relationship("Usuario", back_populates="alumno", uselist=False)
    matriculas = relationship("Matricula", back_populates="alumno")

class Docente(Base):
    __tablename__ = "docentes"
    id_docente = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(15), unique=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    especialidad = Column(String(100))
    telefono = Column(String(20))
    correo = Column(String(100))
    estado = Column(Enum('activo', 'inactivo'), default='activo')

    usuario = relationship("Usuario", back_populates="docente", uselist=False)
    asignaciones = relationship("AsignacionDocente", back_populates="docente")


class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"), unique=True, nullable=True)
    id_alumno = Column(Integer, ForeignKey("alumnos.id_alumno"), unique=True, nullable=True)
    ultimo_acceso = Column(TIMESTAMP, nullable=True)
    estado = Column(Enum('activo', 'inactivo'), default='activo')
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    rol = relationship("Role", back_populates="usuarios")
    docente = relationship("Docente", back_populates="usuario")
    alumno = relationship("Alumno", back_populates="usuario")
    notas_registradas = relationship("Nota", back_populates="usuario_registrador")
    registros_ocr = relationship("RegistroOCR", back_populates="usuario")
    reportes = relationship("ReporteGenerado", back_populates="usuario")


class Curso(Base):
    __tablename__ = "cursos"
    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    nombre_curso = Column(String(100), nullable=False)
    descripcion = Column(Text)
    estado = Column(Enum('activo', 'inactivo'), default='activo')

class Salon(Base):
    __tablename__ = "salones"
    id_salon = Column(Integer, primary_key=True, autoincrement=True)
    grado = Column(String(20), nullable=False)
    seccion = Column(String(10), nullable=False)
    nivel = Column(Enum('Inicial', 'Primaria', 'Secundaria'), nullable=False)
    anio_escolar = Column(Integer, nullable=False) # Year se mapea como Integer
    turno = Column(Enum('mañana', 'tarde', 'noche'))
    capacidad = Column(Integer, default=30)
    estado = Column(Enum('activo', 'inactivo'), default='activo')
    __table_args__ = (UniqueConstraint('grado', 'seccion', 'anio_escolar'),)


class PeriodoAcademico(Base):
    __tablename__ = "periodos_academicos"
    id_periodo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    tipo = Column(Enum('bimestre', 'trimestre'), nullable=False)
    numero_periodo = Column(Integer, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    anio_escolar = Column(Integer, nullable=False)
    estado = Column(Enum('activo', 'cerrado'), default='activo')


class Matricula(Base):
    __tablename__ = "matriculas"
    id_matricula = Column(Integer, primary_key=True, autoincrement=True)
    id_alumno = Column(Integer, ForeignKey("alumnos.id_alumno"), nullable=False)
    id_salon = Column(Integer, ForeignKey("salones.id_salon"), nullable=False)
    fecha_matricula = Column(Date, server_default=func.current_date())
    estado = Column(Enum('activo', 'retirado'), default='activo')

    alumno = relationship("Alumno", back_populates="matriculas")

class AsignacionDocente(Base):
    __tablename__ = "asignacion_docente"
    id_asignacion = Column(Integer, primary_key=True, autoincrement=True)
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"), nullable=False)
    id_curso = Column(Integer, ForeignKey("cursos.id_curso"), nullable=False)
    id_salon = Column(Integer, ForeignKey("salones.id_salon"), nullable=False)
    estado = Column(Enum('activo', 'inactivo'), default='activo')

    docente = relationship("Docente", back_populates="asignaciones")


class Nota(Base):
    __tablename__ = "notas"
    id_nota = Column(Integer, primary_key=True, autoincrement=True)
    id_evaluacion = Column(Integer, ForeignKey("evaluaciones.id_evaluacion"), nullable=False)
    id_matricula = Column(Integer, ForeignKey("matriculas.id_matricula"), nullable=False)
    nota = Column(DECIMAL(5, 2), nullable=False)
    origen = Column(Enum('manual', 'ocr'), default='manual')
    observacion = Column(Text)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    usuario_registrador = relationship("Usuario", back_populates="notas_registradas")


class RegistroOCR(Base):
    __tablename__ = "registros_ocr"
    id_registro = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    estado = Column(Enum('pendiente', 'procesado', 'error'), default='pendiente')
    precision_reconocimiento = Column(DECIMAL(5, 2))
    tiempo_procesamiento_seg = Column(DECIMAL(8, 3))
    caracteres_reconocidos = Column(Integer)
    notas_extraidas = Column(Integer)
    fecha_procesamiento = Column(TIMESTAMP, server_default=func.now())

    usuario = relationship("Usuario", back_populates="registros_ocr")

class ReporteGenerado(Base):
    __tablename__ = "reportes_generados"
    id_reporte = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    tipo_reporte = Column(Enum('boleta_individual', 'reporte_aula', 'reporte_institucional', 'reporte_periodo'), nullable=False)
    id_referencia = Column(Integer)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    tiempo_generacion_seg = Column(DECIMAL(8, 3))
    fecha_generacion = Column(TIMESTAMP, server_default=func.now())

    usuario = relationship("Usuario", back_populates="reportes")

#nota, faltan agregar algunas tablas
