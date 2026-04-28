from app import db
from datetime import datetime
import json

class Auditoria(db.Model):
    __tablename__ = 'auditoria'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idUser'), nullable=True)
    usuario_nombre = db.Column(db.String(100), nullable=True) # Para respaldo rápido
    accion = db.Column(db.String(50), nullable=False) # INSERT, UPDATE, DELETE
    tabla = db.Column(db.String(100), nullable=False)
    registro_id = db.Column(db.Integer, nullable=True)
    valores_anteriores = db.Column(db.Text, nullable=True) # Almacenado como JSON
    valores_nuevos = db.Column(db.Text, nullable=True) # Almacenado como JSON
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('auditorias', lazy=True))

    def __repr__(self):
        return f'<Auditoria {self.accion} on {self.tabla} by {self.usuario_nombre}>'

    @staticmethod
    def log_change(user_id, user_name, action, table, record_id, old_data=None, new_data=None):
        log = Auditoria(
            user_id=user_id,
            usuario_nombre=user_name,
            accion=action,
            tabla=table,
            registro_id=record_id,
            valores_anteriores=json.dumps(old_data) if old_data else None,
            valores_nuevos=json.dumps(new_data) if new_data else None
        )
        db.session.add(log)
        # No hacemos commit aquí porque estamos dentro de una transacción activa
        # que será confirmada por el controlador (route).

