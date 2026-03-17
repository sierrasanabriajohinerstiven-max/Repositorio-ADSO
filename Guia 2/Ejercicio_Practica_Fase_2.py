def es_mayor_de_edad(edad: int) -> bool:
    if edad >= 18:
        return True
    else:
        return False

edad: int = int(input("Ingrese su edad: "))
print(" ")
if es_mayor_de_edad(edad):
    print("Usted es mayor de edad")
else:
    print("Usted es menor de edad")