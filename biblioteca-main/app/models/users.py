from flask_login import UserMixin
from app import db
import qrcode
from io import BytesIO
import base64
from PIL import Image
import os
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    idUser = db.Column(db.Integer, primary_key=True)
    nameUser = db.Column(db.String(80), unique=True, nullable=False)
    passwordUser = db.Column(db.String(255), nullable=False)  # Increased length for hash
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='user')
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Updated relationship with cascade
    perfil = db.relationship('Perfil', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.passwordUser = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordUser, password)


 
    def get_id(self):
        return str(self.idUser)

    def to_dict(self):
        return {
            "idUser": self.idUser,
            "nameUser": self.nameUser,
            "pass": self.passwordUser
        }
    
    def save(self):
        db.add(self)
        db.commit()

    def generate_qr(self):
        # Datos del usuario para el QR
        import json
        from PIL import Image
        user_data = json.dumps({
            'ID': self.idUser,
            'Name': self.nameUser
        })
        print("Generando código QR para el usuario:", user_data)
        # Generar el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(user_data)
        qr.make(fit=True)
        
        # Crear una imagen del QR
        img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')
        
        # Cargar la imagen que se incluirá en el QR
        logo_path = os.path.join(current_app.root_path, 'static', 'img', 'sena.png')
        logo = Image.open(logo_path)
                
        # Calcular el tamaño del logo
        logo_size = 50
        logo = logo.resize((logo_size, logo_size))
        
        # Calcular la posición para centrar el logo en el QR
        pos = ((img_qr.size[0] - logo_size) // 2, (img_qr.size[1] - logo_size) // 2)
        
        # Pegar el logo en el QR
        img_qr.paste(logo, pos)
        
        # Convertir la imagen a base64
        buffered = BytesIO()
        img_qr.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str