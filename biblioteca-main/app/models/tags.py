from app import db
from app.models.posts import post_tags

class Tag(db.Model):
    __tablename__ = 'etiquetas'
    idEtiqueta = db.Column(db.Integer, primary_key=True)
    nombreEtiqueta = db.Column(db.String(100), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relación con Post
    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')

    def __repr__(self):
        return f'<Tag {self.nombreEtiqueta}>'
