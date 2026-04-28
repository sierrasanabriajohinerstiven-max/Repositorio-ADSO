import os
from app import create_app, db
from app.models.users import User

app = create_app()

def init_admin():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Verificar si ya existe un admin
        admin = User.query.filter_by(nameUser='admin').first()
        if not admin:
            print("Creando usuario admin predeterminado...")
            new_admin = User(
                nameUser='admin',
                email='admin@example.com',
                rol='admin'
            )
            # Usar el método set_password para hashear la contraseña
            new_admin.set_password('admin123')
            
            db.session.add(new_admin)
            db.session.flush() # Para obtener el idUser antes del commit

            # Crear perfil inicial para el admin
            from app.models.perfil import Perfil
            new_perfil = Perfil(
                bio="Perfil del administrador del sistema.",
                user_id=new_admin.idUser
            )
            db.session.add(new_perfil)
            
            db.session.commit()
            print("Admin y perfil creados con éxito (admin / admin123)")
        else:
            print("El usuario admin ya existe.")
            # Asegurar que la contraseña esté hasheada
            from werkzeug.security import check_password_hash
            # Intentar verificar 'admin123' con el contenido actual. 
            # Si el contenido actual es plano 'admin123', check_password_hash fallará.
            if not admin.check_password('admin123') and admin.passwordUser == 'admin123':
                print("Detectada contraseña en texto plano para admin. Hasheando...")
                admin.set_password('admin123')
                db.session.commit()
                print("Contraseña del admin hasheada.")

            # Asegurar que tenga perfil si no lo tiene
            from app.models.perfil import Perfil
            if not admin.perfil:
                print("Creando perfil faltante para el admin existente...")
                new_perfil = Perfil(
                    bio="Perfil del administrador del sistema.",
                    user_id=admin.idUser
                )
                db.session.add(new_perfil)
                db.session.commit()
                print("Perfil creado.")

if __name__ == '__main__':
    init_admin()
