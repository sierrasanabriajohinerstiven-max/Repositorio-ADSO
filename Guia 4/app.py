import os
from flask import Flask
from dotenv import load_dotenv

from models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# IMPORTAR RUTAS
from routes import api_bp

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'clave-insegura')

# Conectar base de datos
db.init_app(app)

# Migraciones
migrate = Migrate(app, db)

# JWT
jwt = JWTManager(app)

# REGISTRAR BLUEPRINT
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    puerto = int(os.getenv('PORT', 5000))
    modo_debug = os.getenv('FLASK_DEBUG') == 'True'
    app.run(port=puerto, debug=modo_debug)