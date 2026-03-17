# 1. Creamos una variable en cero ANTES de empezar a repetir
total_ahorrado = 0

# 2. Repetiremos el proceso 3 veces (mes 1, mes 2, mes 3)
for mes in range(1, 4):

# 3. En cada vuelta, le pedimos dinero al usuario
    consignacion = int(input(f"¿Cuánto dinero vas a ahorrar en el mes {mes} ?: "))

# 4. Sumamos lo que ingresó a nuestra caja acumuladora
    total_ahorrado = total_ahorrado + consignacion

# 5. El total se imprime FUERA del bucle (sin indentación) al terminar todas las
print(f"¡Ahorro completado! Tienes un total de: ${total_ahorrado}")