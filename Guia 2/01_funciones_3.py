# Exigimos un Float (decimal) de entrada y garantizamos un Float de salida.
def calcular_iva(precio_base: float) -> float:
    """Calcula y retorna el precio total con un IVA del 19%. """
    iva: float = precio_base * 0.19
    precio_final: float = precio_base + iva
    return precio_final # Expulsa el valor hacia el Call Stack

# El resultado DEBE guardarse en una variable
factura_1: float = calcular_iva(10000.0)
factura_2: float = calcular_iva(50000.0)

print(factura_1)
print(factura_2)