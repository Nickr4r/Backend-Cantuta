# app/core/roles.py
from enum import IntEnum

class RoleID(IntEnum):
    """
    Mapeo exacto de los IDs de la tabla 'roles' en MySQL.
    """
    DIRECTOR = 1
    ADMINISTRATIVO = 2
    DOCENTE = 3
    ESTUDIANTE = 4