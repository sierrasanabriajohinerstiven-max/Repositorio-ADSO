from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    # Pasamos variables al template como keyword arguments
    usuario = {
        'nombre': 'Ana García',
        'email': 'ana@ejemplo.com',
        'activo': True
    }
    articulos = [
        {'titulo': 'Flask desde Cero'},
        {'titulo': 'SQLAlchemy ORM'},
        {'titulo': 'Blueprints'},
    ]
    return render_template(
        'index.html',          # Nombre del archivo en /templates
        usuario=usuario,        # Disponible como {{ usuario }} en el template
        articulos=articulos,    # Disponible como {{ articulos }}
        titulo='Mi Blog'        # String simple
    )
    
if __name__ == '__main__':
    app.run(debug=True)