# 1. Bucle For: Automatizando la repetición
# range(1, 6) genera los números del 1 al 5 (el último número no se incluye)

print ("Iniciando conteo automatizado: ")

for numero in range(1, 6):

# La variable 'numero' cambia su valor automáticamente en cada vuelta

    print (f"Paso actual: {numero}")

# 2. Iterando sobre un texto (cada letra es un paso)

    palabra_clave = "SENA"

print (f"Deletreando la palabra {palabra_clave}:")

for letra in palabra_clave:

# Imprime una letra por cada vuelta del bucle

    print (f"Letra detectada: {letra}")