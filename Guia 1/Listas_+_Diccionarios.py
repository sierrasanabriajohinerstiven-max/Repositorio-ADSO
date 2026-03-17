# 1. Podemos meter diccionarios DENTRO de una lista. Asi funcionan las Bases de D
estudiantes = [
{"nombre": "Ana", "nota": 90},
{"nombre": "Luis", "nota": 50}
]

# 2. Evaluando a todos los estudiantes de forma automática
for persona in estudiantes:
    if persona["nota"] >= 60:
        print(f"{persona['nombre']} ha APROBADO")
    else:
        print(f"{persona['nombre']} ha REPROBADO")