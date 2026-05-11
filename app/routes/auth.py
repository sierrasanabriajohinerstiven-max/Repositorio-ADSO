from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db, bcrypt
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login fallido. Por favor comprueba el email y la contraseña.', 'danger')
            
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validaciones simples
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash('El email ya está registrado. Por favor inicia sesión.', 'warning')
            return redirect(url_for('auth.login'))
            
        user_by_username = User.query.filter_by(username=username).first()
        if user_by_username:
            flash('El nombre de usuario ya está en uso. Por favor elige otro.', 'warning')
            return redirect(url_for('auth.register'))
            
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Tu cuenta ha sido creada exitosamente. ¡Ahora puedes iniciar sesión!', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
