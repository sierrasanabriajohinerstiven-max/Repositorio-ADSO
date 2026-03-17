# 1. Pedimos dos datos diferentes al usuario
tiene_licencia = input("¿Tienes licencia de conducir? (si/no): ")
esta_sobrio = input("¿Has bebido alcohol hoy? (si/no): ")

# 2. Usamos 'and' (Y). AMBAS condiciones deben ser verdad para entrar
if tiene_licencia == "si" and esta_sobrio == "no":
    print("Puedes conducir el vehiculo")

else:
    print("Entregue las llaves. No puede conducir.")