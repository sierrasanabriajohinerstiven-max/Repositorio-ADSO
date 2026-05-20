from app import db
from datetime import datetime
from app.utils.timezone import colombia_now

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=colombia_now)

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'
