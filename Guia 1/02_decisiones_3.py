# A veces, necesitamos tomar una decisión DENTRO de otra decisión.
print(" --- Diagnóstico de Red --- ")
hay_internet = input("¿El módem tiene luces encendidas? (si/no): ")

if hay_internet == "si":
    print("Paso 1: El equipo recibe energía.")

    # Este IF está DENTRO del IF principal. Solo se evalúa si el primero fue "si"
    luz_roja = input("¿Alguna de las luces es color ROJO? (si/no): ")
    if luz_roja == "si":
        print("Fallo detectado: Problema en la fibra óptica. Llame a soporte.")
    else:
        print("Todo normal: Su conexión está operando al 100%.")

else:
    print("Fallo critico: Verifique que el equipo esté conectado a la corriente.")