import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
        print(f"=== DATABASE URI: {db_uri}")
        
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri[len('sqlite:///'):]
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
        
        # Crea las tablas de la base de datos si no existen
        db.create_all()
        print("=== Database tables created successfully!")

        # LIMPIEZA ÚNICA AUTOMÁTICA
        # Usamos un archivo en el directorio persistente 'instance' para asegurar que solo se ejecute UNA vez
        cleanup_flag = os.path.join(app.instance_path, '.db_cleaned')
        if not os.path.exists(cleanup_flag):
            print("=== Iniciando limpieza automática de DB por primera vez ===")
            from app.models.user import User
            from app.models.order import Order, OrderItem
            
            OrderItem.query.delete()
            Order.query.delete()
            User.query.delete()

            admin = User(username='admin', email='marichuyy.m.a@gmail.com', is_admin=True)
            admin.set_password('12872sierra')
            db.session.add(admin)
            db.session.commit()
            
            # Crear la bandera para no volver a limpiar
            with open(cleanup_flag, 'w') as f:
                f.write('cleaned')
            
            print("=== Limpieza completada exitosamente ===")
    
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    
    app.run(host=host, debug=debug)
