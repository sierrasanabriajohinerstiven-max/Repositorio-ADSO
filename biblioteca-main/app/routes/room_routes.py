from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.rooms import Room
from app import db

bp = Blueprint('room', __name__, url_prefix='/room')

@bp.route('/')
@login_required
def index():
    data = Room.query.all()
    return render_template('rooms/index.html', data=data)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.rol != 'admin':
        flash('No tienes permisos para agregar salas.', 'danger')
        return redirect(url_for('room.index'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_room = Room(name=name, description=description)
        db.session.add(new_room)
        db.session.commit()
        
        flash('Sala creada con éxito.', 'success')
        return redirect(url_for('room.index'))
    return render_template('rooms/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para editar salas.', 'danger')
        return redirect(url_for('room.index'))

    room = Room.query.get_or_404(id)
    if request.method == 'POST':
        room.name = request.form['name']
        room.description = request.form['description']
        db.session.commit()
        flash('Sala actualizada con éxito.', 'success')
        return redirect(url_for('room.index'))

    return render_template('rooms/edit.html', room=room)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol.lower() != 'admin':
        flash('Acceso denegado: Se requieren permisos de administrador para eliminar salas.', 'danger')
        return redirect(url_for('room.index'))

    room = Room.query.get_or_404(id)
    try:
        db.session.delete(room)
        db.session.commit()
        flash(f'Sala "{room.name}" eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'No se pudo eliminar la sala. Error: {str(e)}', 'danger')
        
    return redirect(url_for('room.index'))
