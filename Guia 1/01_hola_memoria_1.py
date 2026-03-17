# 1. Salida estatica: El programa "Habla" mostrando texto en pantalla 
print("Iniciando el sistema de diagnostico...")

# 2. Asignacion de estado: Guardando valores en la memoria (Creando "cajas")
temperatura_cpu = 45       #guardamos un numero entero (Integer)
voltaje = 1.2              #guardamos un numero decimal (Float)
estado_sistema = "Estable" #guardamos un texto (String - Siempre en comillas)

# 3. Recuperacion e interpolacion (la letra 'f'antes de las comillas permite met
print(f"Estado actual: {estado_sistema}")
print(f"lecturas: {temperatura_cpu}°C {voltaje}V")

# 4. EL flujo termina cuando no hay mas lineas de codigo
print("Diagnostico finalizado.")
