#Backend/app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.database import get_db

# Importamos los routers de la capa de presentación
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import auth, alumnos

app = FastAPI(
    title="Sistema Cantuta Backend - API",
    description="Backend para la gestión académica con soporte OCR",
    version="1.0.0"
)

#Registramos las rutas del sistema

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(alumnos.router, prefix="/api/v1/alumnos", tags=["Gestión de Alumnos"])

@app.get("/")
def home():
    return {
        "status": "Online", 
        "msg": "Bienvenido al Backend del Sistema Cantuta",
        "docs": "/docs" #documentacion uwu
    }

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "msg": "Conexión a MySQL exitosa!"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}