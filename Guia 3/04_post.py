from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Base de datos simulada en memoria
usuarios_db: list[dict] = []

@app.route('/api/usuarios', methods=['POST'])
def crear_usuario() -> tuple[Response, int]:
    # 1. Extraemos el Payload del Body de la petición HTTP
    datos_entrantes: dict = request.get_json()

    # 2. Resiliencia: Validación del contrato de datos
    if not datos_entrantes or "nombre" not in datos_entrantes:
        return jsonify({"error": "Falta el campo requerido 'nombre'"}), 400  # 400 Bad Request

    # 3. Procesamiento y guardado
    nuevo_usuario = {
        "id": len(usuarios_db) + 1,
        "nombre": datos_entrantes["nombre"],
        "rol": datos_entrantes.get("rol", "Usuario Estandar")
    }

    usuarios_db.append(nuevo_usuario)

    # 4. Retorno de confirmación con código 201 (Created)
    return jsonify({"mensaje": "Usuario creado", "data": nuevo_usuario}), 201


if __name__ == '__main__':
    app.run(debug=True)
