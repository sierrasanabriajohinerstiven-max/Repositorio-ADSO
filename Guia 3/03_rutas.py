from flask import Flask
app = Flask(__name__)

@app.route('/api/temperatura/<float:grados_c>', methods=['GET'])
def convertir_temperatura(grados_c: float) -> str:
    fahrenheit: float = (grados_c * 9/5) + 32
    return f"Temperatura: {grados_c:.2f}°C | Fahrenheit: {fahrenheit:.2f}°F"

if __name__ == '__main__':
    app.run(debug=True)