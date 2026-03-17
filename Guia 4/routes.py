# Archivo: routes.py

from flask import Blueprint, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Usuario, Producto

api_bp = Blueprint('api', __name__)


# ─── REGISTRO ───────────────────────────────────────────────────────────────
@api_bp.route('/usuarios/registrar', methods=['POST'])
def registrar_usuario() -> tuple[Response, int]:
    try:
        payload = request.get_json()

        clave_segura = generate_password_hash(payload['password'])

        nuevo_user = Usuario(
            username=payload['username'],
            password_hash=clave_segura,
            rol=payload.get('rol', 'Operario')
        )

        db.session.add(nuevo_user)
        db.session.commit()

        return jsonify({
            "mensaje": "Usuario registrado exitosamente",
            "data": nuevo_user.serializar()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Fallo de integridad",
            "detalle": str(e)
        }), 400


# ─── LOGIN ───────────────────────────────────────────────────────────────────
@api_bp.route('/login', methods=['POST'])
def login() -> tuple[Response, int]:
    payload = request.get_json()

    usuario = Usuario.query.filter_by(
        username=payload.get('username')
    ).first()

    if usuario and check_password_hash(usuario.password_hash, payload.get('password')):
        token_acceso = create_access_token(identity=usuario.username)

        return jsonify({
            "mensaje": "Login exitoso",
            "token": token_acceso
        }), 200

    return jsonify({
        "error": "Credenciales inválidas"
    }), 401


# ─── LISTAR USUARIOS ─────────────────────────────────────────────────────────
@api_bp.route('/usuarios', methods=['GET'])
def listar_usuarios() -> tuple[Response, int]:
    pagina = request.args.get('page', 1, type=int)

    paginacion = Usuario.query.paginate(
        page=pagina,
        per_page=10,
        error_out=False
    )

    resultado = [u.serializar() for u in paginacion.items]

    return jsonify({
        "pagina_actual": paginacion.page,
        "total_paginas": paginacion.pages,
        "usuarios": resultado
    }), 200


# ─── PERFIL (protegida con JWT) ───────────────────────────────────────────────
@api_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    username = get_jwt_identity()
    usuario = Usuario.query.filter_by(username=username).first()

    return jsonify({
        "username": usuario.username,
        "rol": usuario.rol
    }), 200


# ─── CREAR PRODUCTO (solo Admin) ─────────────────────────────────────────────
@api_bp.route('/productos', methods=['POST'])
@jwt_required()
def crear_producto() -> tuple[Response, int]:

    # Verificar identidad desde el token
    username = get_jwt_identity()
    usuario = Usuario.query.filter_by(username=username).first()

    # Control de rol: solo Admin puede crear productos
    if usuario.rol != "Admin":
        return jsonify({
            "error": "Forbidden: Solo un Administrador puede crear productos"
        }), 403

    try:
        payload = request.get_json()

        nuevo_producto = Producto(
            nombre=payload['nombre'],
            precio=payload['precio'],
            stock=payload.get('stock', 0)
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({
            "mensaje": "Producto creado exitosamente",
            "data": nuevo_producto.serializar()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error al crear producto",
            "detalle": str(e)
        }), 400


# ─── LISTAR PRODUCTOS (protegida con JWT) ────────────────────────────────────
@api_bp.route('/productos', methods=['GET'])
@jwt_required()
def listar_productos() -> tuple[Response, int]:
    productos = Producto.query.all()

    return jsonify({
        "productos": [p.serializar() for p in productos]
    }), 200