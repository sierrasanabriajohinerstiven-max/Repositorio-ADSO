import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

# Normalize sqlite URLs so relative paths are converted to absolute paths.
def _normalize_sqlite_url(url: str) -> str:
    if not url or not url.startswith('sqlite:///'):
        return url

    sqlite_path = url[len('sqlite:///'):]
    if os.path.isabs(sqlite_path):
        return url

    sqlite_path = os.path.abspath(os.path.join(basedir, sqlite_path))
    return 'sqlite:///' + sqlite_path

class Config:
    # Generar una clave aleatoria si no existe para desarrollo local, 
    # pero advertir que en producción DEBE estar definida.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    SQLALCHEMY_DATABASE_URI = _normalize_sqlite_url(os.environ.get('DATABASE_URL', '')) or \
        'sqlite:///' + os.path.join(instance_path, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
