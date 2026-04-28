import sys
import os

# Añadir la ruta del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models.users import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("--- LISTA DE USUARIOS Y ROLES ---")
    for u in users:
        print(f"ID: {u.idUser} | User: {u.nameUser} | Role: '{u.rol}'")
    print("---------------------------------")
