# Si el usuario no envía el parámetro 'moneda', usamos "COP" por defecto
def convertir_moneda(cantidad: float, moneda: str = "COP") -> None:
    print(f"Procesando transacción: {cantidad} en moneda {moneda}")

convertir_moneda(5000.0, "USD") # Reemplaza el valor por defecto
# Como no enviamos moneda, usa "COP"
convertir_moneda(150000.0)
