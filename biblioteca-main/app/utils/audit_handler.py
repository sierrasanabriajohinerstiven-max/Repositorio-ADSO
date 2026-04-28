from sqlalchemy import event
from flask_login import current_user
from app.models.audit import Auditoria
from app import db
from datetime import datetime
import json

def get_current_user_data():
    try:
        from flask_login import current_user
        if current_user and current_user.is_authenticated:
            return current_user.idUser, current_user.nameUser
    except:
        pass
    return None, "Sistema (Automático)"

def sanitize_data(data):
    """Convierte tipos no serializables (como datetime) a strings."""
    if not data: return None
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, datetime):
            sanitized[key] = value.isoformat()
        else:
            sanitized[key] = value
    return sanitized

def register_audit_listeners(model):
    @event.listens_for(model, 'after_insert')
    def receive_after_insert(mapper, connection, target):
        user_id, user_name = get_current_user_data()
        table = target.__tablename__
        record_id = getattr(target, 'idUser', getattr(target, 'idAuthor', getattr(target, 'idPublicacion', getattr(target, 'id', None))))
        
        new_data = {c.name: getattr(target, c.name) for c in target.__table__.columns if c.name != 'passwordUser'}
        
        Auditoria.log_change(user_id, user_name, 'INSERT', table, record_id, None, sanitize_data(new_data))

    @event.listens_for(model, 'after_update')
    def receive_after_update(mapper, connection, target):
        user_id, user_name = get_current_user_data()
        table = target.__tablename__
        record_id = getattr(target, 'idUser', getattr(target, 'idAuthor', getattr(target, 'idPublicacion', getattr(target, 'id', None))))
        
        new_data = {c.name: getattr(target, c.name) for c in target.__table__.columns if c.name != 'passwordUser'}
        
        Auditoria.log_change(user_id, user_name, 'UPDATE', table, record_id, None, sanitize_data(new_data))

    @event.listens_for(model, 'after_delete')
    def receive_after_delete(mapper, connection, target):
        user_id, user_name = get_current_user_data()
        table = target.__tablename__
        record_id = getattr(target, 'idUser', getattr(target, 'idAuthor', getattr(target, 'idPublicacion', getattr(target, 'id', None))))
        
        old_data = {c.name: getattr(target, c.name) for c in target.__table__.columns if c.name != 'passwordUser'}
        
        Auditoria.log_change(user_id, user_name, 'DELETE', table, record_id, sanitize_data(old_data), None)
