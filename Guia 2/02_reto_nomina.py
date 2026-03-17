def calcular_salario_neto(salario_base: float, bonificacion: float = 0.0) -> float:
    descuento_salud: float = salario_base * 0.08
    descuento_pension: float = salario_base * 0.08
    salario_neto: float = salario_base - descuento_salud - descuento_pension + bonificacion
    return salario_neto

salario_base: float = float(input("Ingrese el salario base: "))
print("\n")
bonificacion: float = float(input("Ingrese la bonificacion: "))
print("\n")

salario_neto: float = calcular_salario_neto(salario_base, bonificacion)
print(f"El salario neto es: {salario_neto}")