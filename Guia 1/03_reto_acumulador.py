print("--- Reto Acumulador ---")
print(" ")
print("Caja registradora")
print(" ")
acumuladora = 0
for producto in range(1, 6):
    precio = float(input("Ingrese el precio del producto: "))
    acumuladora = acumuladora + precio
print(" ")
print(f"El total de la compra es: {acumuladora}")
print(" ")
print("--- Fin del programa ---")