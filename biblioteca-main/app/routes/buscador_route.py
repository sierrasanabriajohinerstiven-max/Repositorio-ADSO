from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models.posts import Post
from app.models.authors import Author
from app.models.rooms import Room

bp = Blueprint('buscador', __name__, url_prefix='/buscador')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    query = request.args.get('q', '')
    if not query:
        return render_template('buscador_resultados.html', query='', results={})

    # Buscar en Posts
    posts = Post.query.filter(
        (Post.tituloPublicacion.contains(query)) | 
        (Post.contenidoPublicacion.contains(query))
    ).all()

    # Buscar en Autores
    # Nota: El modelo Author tiene nameAuthor, no name. 
    # En search_route anteriormente puse Author.name por error. Corrijo a Author.nameAuthor
    autores = Author.query.filter(Author.nameAuthor.contains(query)).all()

    # Buscar en Salas
    salas = Room.query.filter(
        (Room.name.contains(query)) | 
        (Room.description.contains(query))
    ).all()

    results = {
        'publicaciones': posts,
        'autores': autores,
        'salas': salas
    }

    return render_template('buscador_resultados.html', query=query, results=results)
