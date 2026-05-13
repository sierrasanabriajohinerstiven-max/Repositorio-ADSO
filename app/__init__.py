# pyrefly: ignore [missing-import]
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# pyrefly: ignore [missing-import]
from flask_login import LoginManager
# pyrefly: ignore [missing-import]
from flask_bcrypt import Bcrypt

# Cargar variables de entorno desde .env
load_dotenv()
from config import Config
# pyrefly: ignore [missing-import]
from flask_wtf.csrf import CSRFProtect
# pyrefly: ignore [missing-import]
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Por favor inicia sesión para acceder a esta página.'
login.login_message_category = 'info'
csrf = CSRFProtect()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    from app.routes.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.routes.admin import admin as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
