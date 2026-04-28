from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.posts import Post
from app.models.tags import Tag
from app import db

bp = Blueprint('post', __name__, url_prefix='/Post')

@bp.route('/')
@login_required
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', data=posts)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.rol != 'admin':
        flash('No tienes permisos para añadir publicaciones.', 'danger')
        return redirect(url_for('post.index'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')
        id_author = request.form.get('idAuthor')
        tag_ids = request.form.getlist('etiquetas')
        
        nuevo_post = Post(tituloPublicacion=titulo, contenidoPublicacion=contenido, idAuthor=id_author)
        
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                nuevo_post.tags.append(tag)
        
        db.session.add(nuevo_post)
        db.session.commit()
        flash('Publicación añadida con éxito', 'success')
        return redirect(url_for('post.index'))
    
    from app.models.authors import Author
    tags = Tag.query.all()
    authors = Author.query.all()
    return render_template('posts/add.html', etiquetas=tags, autores=authors)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para editar publicaciones.', 'danger')
        return redirect(url_for('post.index'))

    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.tituloPublicacion = request.form.get('titulo')
        post.contenidoPublicacion = request.form.get('contenido')
        
        tag_ids = request.form.getlist('etiquetas')
        post.tags = []
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
                 
        db.session.commit()
        flash('Publicación actualizada con éxito', 'success')
        return redirect(url_for('post.index'))
    
    tags = Tag.query.all()
    return render_template('posts/edit.html', publicacion=post, etiquetas=tags)

@bp.route('/list/<int:id>')
@login_required
def list(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/list.html', publicacion=post)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para eliminar publicaciones.', 'danger')
        return redirect(url_for('post.index'))

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Publicación eliminada', 'warning')
    return redirect(url_for('post.index'))

@bp.route('/filter', methods=['GET', 'POST'])
@login_required
def filter():
    if request.method == 'POST':
        tag_id = request.form.get('etiqueta')
        tag = Tag.query.get(tag_id)
        if tag:
            posts = tag.posts
        else:
            posts = []
        return render_template('posts/index.html', data=posts)
    
    tags = Tag.query.all()
    return render_template('posts/filter.html', etiquetas=tags)
