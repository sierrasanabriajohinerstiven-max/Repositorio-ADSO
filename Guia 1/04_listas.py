# 1. Creación de una lista: Se usan corchetes [] y se separan por comas
inventario_frutas = ["Manzana", "Pera", "Mango", "Banano"]

# 2. Accediendo a un elemento especifico: ¡Los programadores empezamos a contar
print(f"La primera fruta es: {inventario_frutas[0]}") # Imprime Manzana
print(f"La tercera fruta es: {inventario_frutas[2]}") # Imprime Mango

# 3. La verdadera magia: Combinando Listas y el ciclo For
print(" --- Imprimiendo viñetas automáticas --- ")

# Por cada 'fruta' individual dentro de la lista 'inventario_frutas', haz lo sigu
for fruta in inventario_frutas:
    print(f"- {fruta} disponible en bodega.")