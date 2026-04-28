from app import db

# Tabla de asociación para la relación Muchos a Muchos entre Posts y Tags
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('publicaciones.idPublicacion'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('etiquetas.idEtiqueta'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'publicaciones'
    idPublicacion = db.Column(db.Integer, primary_key=True)
    tituloPublicacion = db.Column(db.String(255), nullable=False)
    contenidoPublicacion = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relación con Autor (Esencial)
    idAuthor = db.Column(db.Integer, db.ForeignKey('authors.idAuthor'), nullable=True)
    autor = db.relationship('Author', backref=db.backref('publicaciones', lazy=True))
    
    # Relación con Tag
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

    def __repr__(self):
        return f'<Post {self.tituloPublicacion}>'
