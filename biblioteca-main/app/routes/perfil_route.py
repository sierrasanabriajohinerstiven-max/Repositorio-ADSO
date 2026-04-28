from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.perfil import Perfil
from app.models.users import User
from app import db

bp = Blueprint('perfil', __name__, url_prefix='/perfil')

@bp.route('/')
@login_required
def index():
    # Solo admins pueden ver todos los perfiles, o tal vez todos pueden listarlos? 
    # Sigamos el deseo de que el usuario solo puede ver el contenido.
    perfiles = Perfil.query.all()
    return render_template('perfil/index.html', perfiles=perfiles)

@bp.route('/mi-perfil')
@login_required
def mi_perfil():
    perfil = Perfil.query.filter_by(user_id=current_user.idUser).first()
    if not perfil:
        return redirect(url_for('perfil.add'))
    return render_template('perfil/detail.html', perfil=perfil)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    # Permitir que un admin cree un perfil para otro usuario (pasando user_id)
    # o que un usuario cree el suyo propio
    target_user_id = request.args.get('user_id', current_user.idUser, type=int)
    
    if current_user.rol != 'admin' and target_user_id != current_user.idUser:
        flash('No tienes permiso para crear este perfil.', 'danger')
        return redirect(url_for('post.index'))

    existing_perfil = Perfil.query.filter_by(user_id=target_user_id).first()
    if existing_perfil:
        if target_user_id == current_user.idUser:
            flash('Ya tienes un perfil creado.', 'warning')
            return redirect(url_for('perfil.mi_perfil'))
        else:
            flash('Este usuario ya tiene un perfil.', 'warning')
            return redirect(url_for('user.index'))

    if request.method == 'POST':
        bio = request.form.get('bio', '')
        new_perfil = Perfil(bio=bio, user_id=target_user_id)
        db.session.add(new_perfil)
        db.session.commit()

        flash('Perfil creado exitosamente.', 'success')
        if target_user_id == current_user.idUser:
            return redirect(url_for('perfil.mi_perfil'))
        else:
            return redirect(url_for('user.index'))

    return render_template('perfil/add.html', user_id=target_user_id)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    perfil = Perfil.query.get_or_404(id)

    # Solo el dueño o un admin pueden editar
    if perfil.user_id != current_user.idUser and current_user.rol != 'admin':
        flash('No tienes permiso para editar este perfil.', 'danger')
        return redirect(url_for('post.index'))

    if request.method == 'POST':
        perfil.bio = request.form.get('bio', '')
        db.session.commit()

        flash('Perfil actualizado exitosamente.', 'success')
        return redirect(url_for('perfil.detail', id=perfil.idPerfil))

    return render_template('perfil/edit.html', perfil=perfil)

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    perfil = Perfil.query.get_or_404(id)
    return render_template('perfil/detail.html', perfil=perfil)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    perfil = Perfil.query.get_or_404(id)
    
    # Solo el admin puede eliminar perfiles arbitrarios
    if current_user.rol != 'admin':
        flash('No tienes permiso para eliminar perfiles.', 'danger')
        return redirect(url_for('perfil.index'))

    db.session.delete(perfil)
    db.session.commit()
    flash('Perfil eliminado exitosamente.', 'warning')
    return redirect(url_for('perfil.index'))
