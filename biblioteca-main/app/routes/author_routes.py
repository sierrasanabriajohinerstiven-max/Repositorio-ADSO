from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.authors import Author
from app import db

bp = Blueprint('author', __name__, url_prefix='/Author')

@bp.route('/')
@login_required
def index():
    authors = Author.query.all()   
    return render_template('authors/index.html', data=authors)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.rol != 'admin':
        flash('No tienes permisos para agregar autores.', 'danger')
        return redirect(url_for('author.index'))

    if request.method == 'POST':
        name = request.form.get('nameAuthor')
        nationality = request.form.get('nationalityAuthor')
        
        if not name or not nationality:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('author.add'))

        new_author = Author(nameAuthor=name, nationalityAuthor=nationality)
        db.session.add(new_author)
        db.session.commit()
        flash('Autor agregado con éxito.', 'success')
        return redirect(url_for('author.index'))

    return render_template('authors/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para editar autores.', 'danger')
        return redirect(url_for('author.index'))

    author = Author.query.get_or_404(id)

    if request.method == 'POST':
        author.nameAuthor = request.form.get('nameAuthor')
        author.nationalityAuthor = request.form.get('nationalityAuthor')
        db.session.commit()
        flash('Autor actualizado con éxito.', 'success')
        return redirect(url_for('author.index'))

    return render_template('authors/edit.html', author=author)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol.lower() != 'admin':
        flash('No tienes permisos administrativos para eliminar registros.', 'danger')
        return redirect(url_for('author.index'))

    author = Author.query.get_or_404(id)
    try:
        db.session.delete(author)
        db.session.commit()
        flash(f'Autor "{author.nameAuthor}" eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'No se pudo eliminar al autor. Es posible que tenga libros asociados. Error: {str(e)}', 'danger')
    
    return redirect(url_for('author.index'))
