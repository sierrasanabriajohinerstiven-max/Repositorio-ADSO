import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# -----------------------------
# CAPA DE NEGOCIO (POO)
# -----------------------------

class Producto:
    def __init__(self):
        self.__productos: list[dict] = []

    def crear_producto(self, nombre: str, precio: float) -> dict:
        nuevo = {
            "id": len(self.__productos) + 1,
            "nombre": nombre,
            "precio": precio
        }
        self.__productos.append(nuevo)
        return nuevo

    def listar_productos(self) -> list[dict]:
        return self.__productos


# Instancia única (Singleton)
gestor_productos = Producto()

# -----------------------------
# CAPA DE TRANSPORTE (Flask)
# -----------------------------

@app.route('/api/productos', methods=['GET'])
def obtener_productos() -> tuple[Response, int]:
    datos = gestor_productos.listar_productos()
    return jsonify({
        "total": len(datos),
        "productos": datos
    }), 200


@app.route('/api/productos', methods=['POST'])
def agregar_producto() -> tuple[Response, int]:
    try:
        payload = request.get_json()

        if not payload or "nombre" not in payload or "precio" not in payload:
            return jsonify({"error": "Estructura JSON invalida"}), 400

        nuevo_producto = gestor_productos.crear_producto(
            payload["nombre"],
            float(payload["precio"])
        )

        return jsonify({
            "mensaje": "Producto creado correctamente",
            "data": nuevo_producto
        }), 201

    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5000))

    app.run(host="0.0.0.0", port=port, debug=debug_mode)