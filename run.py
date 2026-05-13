import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crea las tablas de la base de datos si no existen
        db.create_all()
    
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    
    app.run(host=host, debug=debug)
