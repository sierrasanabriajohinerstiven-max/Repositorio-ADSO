# 1. Creación de un diccionario: Se usan llaves {} y el formato "Clave": "Valor"
aprendiz = {
"nombre": "Carlos",
"edad": 25,
"curso": "Programación",
"activo": True

}

# 2. Accediendo a datos específicos usando la "Etiqueta" (Clave)
print(f"Nombre: {aprendiz['nombre']}")

# 3. Modificando un valor existente y agregando nuevos
aprendiz["edad"] = 26
aprendiz["ciudad"] = "Bogota" # Nueva clave (Python la crea automaticamente si no existe)
