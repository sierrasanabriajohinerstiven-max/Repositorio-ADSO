# 1. Entrada de datos: El programa se pausa y espera a que el usuario escriba algo
# Nota: input() siempre guarda texto. Si queremos números, lo envolvemos en int()
edad_usuario = int(input("Por favor, ingresa tu edad en números: ") )

# 2. Evaluación lógica: El programa analiza el dato ingresado
print("Evaluando permisos de acceso ... ")

# 3. Bifurcación (If / Elif / Else): El código toma un solo camino
print("Acceso concedido: Eres mayor de edad.")
if edad_usuario >= 18:
    print("Acceso concedido: Eres mayor de edad.")

# Si la condicion es verdadera, entra a este bloque

elif edad_usuario >= 13:
# Si la de arriba fue falsa, pero esta es VERDADERA, entra aquí (Cortocircuito)
    print("A Acceso restringido: Eres adolescente, necesitas permiso de un tutor. ")

else:
# Si NINGUNA de las anteriores fue verdadera, por descarte entra aquí
    print("Acceso denegado: Eres menor de edad. ")

# 4. Esta línea no tiene espacios a la izquierda, así que se ejecuta SIEMPRE
print("Gracias por usar el sistema. ")



