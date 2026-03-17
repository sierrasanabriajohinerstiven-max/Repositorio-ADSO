# 1. Creación de una tupla: A diferencia de las listas, se usan PARÉNTESIS ()
coordenadas_bogota = (4.7110, -74.0721)
meses_año = ("Enero", "Febrero", "Marzo")

# 2. Se accede exactamente igual que a una lista (empezando desde el cero)
print(f"La latitud de Bogota es: {coordenadas_bogota[0]}")
print(f"El primer mes es: {meses_año[0]}")

# 3. LO QUE NO SE PUEDE HACER (Inmutabilidad)
# Si intentas: coordenadas_bogota[0] = 5.0 -> ERROR CRÍTICO.