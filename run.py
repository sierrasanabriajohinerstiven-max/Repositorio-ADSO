from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crea las tablas de la base de datos si no existen
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
