#Backend/app/infrastructure/basedatos.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Cargar variables de entorno
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Crear el motor de conexión
# El motor permite a SQLAlchemy comunicarse con MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Crear una fábrica de sesiones
# Cada vez que alguien entra al sistema, le daremos una sesión nueva
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase base para los modelos
# De esta clase heredarán todos nuestros modelos de la base de datos
Base = declarative_base()

# 5. Dependencia para los Endpoints
# Esta función abre una conexión y la cierra automáticamente al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()