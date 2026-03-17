def calcular_area_rectangulo(base: float, altura: float) -> float:
    area_rectangulo: float = base * altura
    return area_rectangulo

base: float = float(input("Ingrese la base del rectangulo: "))
print(" ")
altura: float = float(input("Ingrese la altura del rectangulo: "))
print(" ")

area_total: float = calcular_area_rectangulo(base, altura)
print(f"El area total del rectangulo es: {area_total}")