from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file, flash
from flask_login import login_required, current_user
from app.models.users import User
from app.models.perfil import Perfil
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('user', __name__, url_prefix='/User')

@bp.route('/')
@login_required
def index():
    if current_user.rol != 'admin':
        flash('No tienes permisos para ver la lista de usuarios.', 'danger')
        return redirect(url_for('post.index'))
    data = User.query.all()
    return render_template('users/index.html', data=data)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    # Solo permitir acceso si no está logueado (registro) o si es admin
    if current_user.is_authenticated and current_user.rol != 'admin':
        flash('No tienes permisos para agregar usuarios adicionales.', 'danger')
        return redirect(url_for('post.index'))

    if request.method == 'POST':
        nameUser = request.form['nameUser']
        passwordUser = request.form['passwordUser']
        email = request.form['email']
        
        # El rol solo puede ser elegido por un admin. Si no, es siempre 'user'.
        if current_user.is_authenticated and current_user.rol == 'admin':
            rol = request.form.get('rol', 'user')
        else:
            rol = 'user'
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(nameUser=nameUser).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('user.add'))
            
        new_user = User(nameUser=nameUser, email=email, rol=rol)
        new_user.set_password(passwordUser)
        db.session.add(new_user)
        db.session.commit()
        
        if not current_user.is_authenticated:
            # Login automático para el nuevo usuario
            from flask_login import login_user
            login_user(new_user)
            flash('Cuenta creada con éxito. Por favor completa tu perfil.', 'success')
            return redirect(url_for('perfil.add'))
        else:
            # Si lo creó un admin, vuelve a la lista
            flash(f'Usuario {nameUser} creado con éxito.', 'success')
            return redirect(url_for('user.index'))

    return render_template('users/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para editar usuarios.', 'danger')
        return redirect(url_for('post.index'))

    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.nameUser = request.form['nameUser']
        if request.form['passwordUser']: # Only update if a password was provided
            user.set_password(request.form['passwordUser'])
        user.email = request.form['email']
        user.rol = request.form.get('rol', user.rol)
        db.session.commit()        
        flash('Usuario actualizado con éxito.', 'success')
        return redirect(url_for('user.index'))

    return render_template('users/edit.html', user=user)

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    # Un usuario puede ver su propio detalle o un admin cualquiera
    if current_user.rol != 'admin' and current_user.idUser != id:
        flash('No tienes permisos para ver este detalle.', 'danger')
        return redirect(url_for('post.index'))
        
    user = User.query.get_or_404(id)
    return render_template('users/detail.html', user=user)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.rol.lower() != 'admin':
        flash('No tienes privilegios para eliminar usuarios registrados.', 'danger')
        return redirect(url_for('user.index'))

    if current_user.idUser == id:
        flash('No puedes eliminar tu propia cuenta administrativa.', 'warning')
        return redirect(url_for('user.index'))

    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'Usuario {user.nameUser} eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar usuario: {str(e)}', 'danger')
        
    return redirect(url_for('user.index'))

@bp.route('/qr/<int:id>')
@login_required
def generate_qr(id):
    user = User.query.get_or_404(id)
    qr_code_base64 = user.generate_qr()
    qr_code_img = base64.b64decode(qr_code_base64)
    return send_file(BytesIO(qr_code_img), mimetype='image/png')

@bp.route('/read_qr', methods=['POST'])
@login_required
def read_qr():
    from pyzbar.pyzbar import decode
    from PIL import Image
    
    if 'qr_image' not in request.files:
        flash('No se ha proporcionado una imagen de QR', 'danger')
        return redirect(url_for('user.index'))

    qr_image = request.files['qr_image']
    img = Image.open(qr_image)
    decoded_objects = decode(img)

    if not decoded_objects:
        flash('No se pudo leer el código QR', 'danger')
        return redirect(url_for('user.index'))

    qr_data = decoded_objects[0].data.decode('utf-8')
    user_data = json.loads(qr_data)
    user_id = user_data.get('ID')

    if not user_id:
        flash('El código QR no contiene un ID de usuario válido', 'danger')
        return redirect(url_for('user.index'))

    user = User.query.get(user_id)
    if not user:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('user.index'))

    return render_template('users/detail.html', user=user)
