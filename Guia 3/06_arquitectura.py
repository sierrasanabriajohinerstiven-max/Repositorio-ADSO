import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CAPA DE LÓGICA DE NEGOCIO (Core / POO) ---
class InventarioTrapiche:
    def __init__(self):
        self.productos: list[dict] = []

    def agregar_lote(self, tipo: str, kilos: float) -> dict:
        lote = {
            "id": len(self.productos) + 1,
            "tipo": tipo,
            "kilos": kilos
        }
        self.productos.append(lote)
        return lote

    def obtener_todos(self) -> list[dict]:
        return self.productos


# Instanciación del Singleton (Gestor único en RAM)
gestor_inventario = InventarioTrapiche()


# --- CAPA DE TRANSPORTE (Controladores / Flask) ---

@app.route('/api/inventario', methods=['GET'])
def ver_inventario() -> tuple[Response, int]:
    datos = gestor_inventario.obtener_todos()
    return jsonify({
        "total": len(datos),
        "lotes": datos
    }), 200


@app.route('/api/inventario', methods=['POST'])
def registrar_lote() -> tuple[Response, int]:
    try:
        payload = request.get_json()

        nuevo_lote = gestor_inventario.agregar_lote(
            payload["tipo"],
            payload["kilos"]
        )

        return jsonify({
            "mensaje": "Lote registrado",
            "data": nuevo_lote
        }), 201

    except (KeyError, TypeError):
        return jsonify({
            "error": "Estructura JSON invalida."
        }), 400


if __name__ == '__main__':
    app.run(
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "False") == "True"
    )