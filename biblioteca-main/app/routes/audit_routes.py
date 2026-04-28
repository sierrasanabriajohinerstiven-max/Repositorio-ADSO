from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.models.audit import Auditoria
from functools import wraps
from flask import abort

bp = Blueprint('audit', __name__, url_prefix='/auditoria')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def index():
    # Obtener los últimos 100 registros de auditoría
    logs = Auditoria.query.order_by(Auditoria.fecha.desc()).limit(100).all()
    return render_template('audit/index.html', logs=logs)
