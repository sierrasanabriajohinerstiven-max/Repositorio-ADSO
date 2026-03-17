carrito_compras = ["Leche", "Huevos", "Pan"]
print(f"Carrito inicial: {carrito_compras}")

# 1. Agregar al final (.append)
carrito_compras.append("Café")
print(f"Agregué Café: {carrito_compras}")

# 2. Eliminar un elemento especifico (.remove)
carrito_compras.remove("Leche")
print(f"Quité la Leche: {carrito_compras}")

# 3. Cambiar un elemento sabiendo su posición (Cajón 0)
carrito_compras[0] = "Huevos Campesinos"

print(f"Cambié los huevos normales: {carrito_compras}")