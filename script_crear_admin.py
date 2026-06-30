# create_admin.py
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal # Importamos tu fábrica de sesiones
from app.domain.models import Usuario, Role
from app.core.security import get_password_hash # Tu función de encriptación

def create_initial_admin():
    db = SessionLocal()
    try:
        # 1. Verificar si el rol de Director existe
        # (Basado en tu SQL, el ID 1 debería ser Director)
        admin_role = db.query(Role).filter(Role.id_rol == 1).first()
        if not admin_role:
            print("Error: El rol de Director (ID 1) no existe en la base de datos.")
            print("Asegúrate de haber ejecutado tu script SQL primero.")
            return

        # 2. Verificar si ya existe un admin para no duplicar
        admin_exists = db.query(Usuario).filter(Usuario.username == "admin").first()
        if admin_exists:
            print("El usuario 'admin' ya existe.")
            return

        # 3. Crear el primer administrador
        print("Creando usuario administrador inicial...")
        
        # AQUÍ DEFINES LA CONTRASEÑA INICIAL
        password_plana = "admin1234" 
        hashed_password = get_password_hash(password_plana)

        new_admin = Usuario(
            username="admin",
            password_hash=hashed_password,
            id_rol=1, # Rol de Director
            estado="activo"
        )

        db.add(new_admin)
        db.commit()
        
        print("------------------------------------------")
        print("¡Usuario Administrador creado con éxito!")
        print(f"Usuario: admin")
        print(f"Password: {password_plana}")
        print("------------------------------------------")
        print("IMPORTANTE: Cambia esta contraseña al entrar por primera vez.")

    except Exception as e:
        print(f"Hubo un error al crear el admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()