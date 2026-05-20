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
login.login_message = 'Necesita iniciar sesión para acceder al catálogo y carrito.'
login.login_message_category = 'warning'
csrf = CSRFProtect()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Aseguramos que la carpeta de instancia exista para SQLite
    os.makedirs(app.instance_path, exist_ok=True)
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri[len('sqlite:///'):]
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    from app.utils.timezone import format_datetime
    app.add_template_filter(format_datetime)

    from app.routes.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.routes.admin import admin as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Context processor para inyectar notificaciones en todos los templates
    @app.context_processor
    def inject_notifications():
        from flask_login import current_user as ctx_user
        if ctx_user.is_authenticated and not ctx_user.is_admin:
            from app.models.notification import Notification
            unread = Notification.query.filter_by(user_id=ctx_user.id, is_read=False).count()
            recent_notifications = Notification.query.filter_by(user_id=ctx_user.id)\
                .order_by(Notification.created_at.desc()).limit(10).all()
            return dict(unread=unread, recent_notifications=recent_notifications)
        return dict(unread=0, recent_notifications=[])

    return app
