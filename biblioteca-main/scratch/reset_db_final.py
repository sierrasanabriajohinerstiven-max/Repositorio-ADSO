import sys
import os

# Añadir la ruta del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.users import User
from app.models.authors import Author
from app.models.rooms import Room
from app.models.tags import Tag
from app.models.perfil import Perfil

app = create_app()

with app.app_context():
    # 1. Crear todas las tablas
    print("Creando tablas...")
    db.create_all()

    # 2. Crear Administrador
    print("Creando usuario administrador...")
    admin = User(nameUser='admin', email='admin@ejemplo.com', rol='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.flush() # Para obtener el idUser

    # 3. Crear Perfil para Admin
    admin_perfil = Perfil(bio='Administrador principal del sistema de biblioteca. Control total de registros y auditoría.', user_id=admin.idUser)
    db.session.add(admin_perfil)

    # 4. Crear Datos de Ejemplo
    print("Poblando datos iniciales...")
    
    # Autores
    gabo = Author(nameAuthor='Gabriel García Márquez', nationalityAuthor='Colombiana')
    borges = Author(nameAuthor='Jorge Luis Borges', nationalityAuthor='Argentina')
    db.session.add_all([gabo, borges])

    # Salas
    sala_a = Room(name='Sala de Lectura A', description='Zona de silencio total y alta concentración.', status='Disponible')
    sala_v = Room(name='Sala Virtual', description='Equipada con estaciones de trabajo de alto rendimiento.', status='Disponible')
    db.session.add_all([sala_a, sala_v])

    # Etiquetas
    tag1 = Tag(nombreEtiqueta='Clásicos')
    tag2 = Tag(nombreEtiqueta='Tecnología')
    tag3 = Tag(nombreEtiqueta='Realismo Mágico')
    db.session.add_all([tag1, tag2, tag3])

    # 5. Guardar todo
    db.session.commit()
    print("¡Base de datos reiniciada e inicializada con éxito!")
    print("Acceso Admin: admin / admin123")
