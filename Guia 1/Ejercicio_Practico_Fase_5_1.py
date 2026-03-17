print("--dias_semana--")
print(" ")
dias_semana = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")

print("Ingresa un numero del 1 al 7 para determinar el dia de la semana: ")

numero = int(input())

print("El dia del numero ", numero, "es ", dias_semana[numero - 1])

print("Intentando usar append() en la tupla...")

try:
    dias_semana.append("OtroDia")
except AttributeError as error:
    print("Se produjo un error:", error)
