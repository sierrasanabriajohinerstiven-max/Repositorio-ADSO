from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.tags import Tag
from app import db

bp = Blueprint('tag', __name__, url_prefix='/Tag')

@bp.route('/')
@login_required
def index():
    tags = Tag.query.all()
    return render_template('tags/index.html', data=tags)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.rol != 'admin':
        flash('No tienes permisos para agregar etiquetas.', 'danger')
        return redirect(url_for('tag.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('tag.add'))
            
        nuevo_tag = Tag(nombreEtiqueta=nombre)
        db.session.add(nuevo_tag)
        db.session.commit()
        flash('Etiqueta creada con éxito', 'success')
        return redirect(url_for('tag.index'))
    
    return render_template('tags/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para editar etiquetas.', 'danger')
        return redirect(url_for('tag.index'))

    tag = Tag.query.get_or_404(id)
    if request.method == 'POST':
        tag.nombreEtiqueta = request.form.get('nombre')
        db.session.commit()
        flash('Etiqueta actualizada con éxito', 'success')
        return redirect(url_for('tag.index'))
    
    return render_template('tags/edit.html', etiqueta=tag)

@bp.route('/list/<int:id>')
@login_required
def list(id):
    tag = Tag.query.get_or_404(id)
    posts = tag.posts
    return render_template('tags/list.html', etiqueta=tag, publicaciones=posts)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para eliminar etiquetas.', 'danger')
        return redirect(url_for('tag.index'))

    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Etiqueta eliminada', 'warning')
    return redirect(url_for('tag.index'))

@bp.route('/filter', methods=['GET', 'POST'])
@login_required
def filter():
    if request.method == 'POST':
        query = request.form.get('query')
        tags = Tag.query.filter(Tag.nombreEtiqueta.contains(query)).all()
        return render_template('tags/index.html', data=tags)
    
    return render_template('tags/filter.html')
