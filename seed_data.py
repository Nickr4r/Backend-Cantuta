# seed_data.py
from faker import Faker
from app.infrastructure.database import SessionLocal
from app.domain.models import Alumno, Docente, PersonalAdministrativo
import random

fake = Faker() # Configurado para datos de Perú
db = SessionLocal()

def seed_data():
    print("🚀 Iniciando generación de datos...")

    # 1. Crear 2000 Alumnos
    print("Generando 2000 alumnos...")
    for _ in range(2000):
        alumno = Alumno(
            dni=fake.unique.numerify(text='########'),
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            fecha_nacimiento=fake.date_of_birth(minimum_age=5, maximum_age=17),
            sexo=random.choice(['M', 'F']),
            correo=fake.unique.email()
        )
        db.add(alumno)
    
    # 2. Crear 400 Docentes
    print("Generando 400 docentes...")
    for _ in range(400):
        docente = Docente(
            dni=fake.unique.numerify(text='########'),
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            especialidad=fake.job(),
            correo=fake.unique.email()
        )
        db.add(docente)

    # 3. Crear 100 Personal
    print("Generando 100 administrativos...")
    for _ in range(100):
        personal = PersonalAdministrativo(
            dni=fake.unique.numerify(text='########'),
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            cargo=fake.job(),
            correo=fake.unique.email()
        )
        db.add(personal)

    db.commit()
    print("✅ ¡Datos generados con éxito!")

if __name__ == "__main__":
    seed_data()