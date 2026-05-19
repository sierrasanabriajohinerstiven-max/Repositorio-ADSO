import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Debug: mostrar la URI de la base de datos
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
        print(f"=== DATABASE URI: {db_uri}")
        
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri[len('sqlite:///'):]
            db_dir = os.path.dirname(db_path)
            print(f"=== DB file path: {db_path}")
            print(f"=== DB directory: {db_dir}")
            print(f"=== DB dir exists: {os.path.exists(db_dir)}")
            print(f"=== DB dir writable: {os.access(db_dir, os.W_OK) if os.path.exists(db_dir) else 'N/A'}")
            
            # Asegurar que el directorio existe
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
                print(f"=== DB dir created/verified: {os.path.exists(db_dir)}")
        
        # Crea las tablas de la base de datos si no existen
        db.create_all()
        print("=== Database tables created successfully!")
    
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    
    app.run(host=host, debug=debug)
