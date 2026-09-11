# Backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware # 1. Importamos CORS
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.database import get_db

# Importamos los routers de la capa de presentación
from app.api.v1.endpoints import auth, alumnos, docentes, personal

app = FastAPI(
    title="Sistema Cantuta Backend - API",
    description="Backend para la gestión académica con soporte OCR",
    version="1.0.0"
)

# 2. Configuramos los orígenes permitidos (tu frontend en Next.js)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.2:3000",

]

# 3. Añadimos el middleware a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todas las cabeceras (Headers)
)

# Registramos las rutas del sistema
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(alumnos.router, prefix="/api/v1/alumnos", tags=["Gestión de Alumnos"])
app.include_router(docentes.router, prefix="/api/v1/docentes", tags=["Gestión de Docentes"])
app.include_router(personal.router, prefix="/api/v1/personal", tags=["Gestión de Personal"])

@app.get("/")
def home():
    return {
        "status": "Online", 
        "msg": "Bienvenido al Backend del Sistema Cantuta",
        "docs": "/docs"
    }

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "msg": "Conexión a MySQL exitosa!"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}