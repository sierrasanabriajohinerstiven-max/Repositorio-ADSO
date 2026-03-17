# 1. Importamos la clase principal del framework
from flask import Flask

# 2. INSTANCIACIÓN: Creamos el objeto servidor.
# __name__ le dice a Flask donde buscar los archivos internos del proyecto
app = Flask(__name__)

# 3. ENRUTAMIENTO: El decorador '@' mapea una URL de red con una función en RAM.
@app.route('/')  # métodos = ['GET']
def home():
    """Función que se ejecuta cuando el cliente hace GET a la raíz del sitio."""
    return "<h1>Sistema de Control Agroindustrial Activo</h1>"

# 4. EJECUCIÓN DEL BUCLE DE ESCUCHA
if __name__ == '__main__':
    print("Iniciando servidor en [http://127.0.0.1:5000]")
    app.run(host='0.0.0.0', port=5000, debug=True)