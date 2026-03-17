# A veces necesitamos saber exactamente QUE tipo de dato tiene una caja
# Usamos la funcion type() para que Python nos revele el secreto

dato_desconocido = "100" # !Atencion! Es un numero, pero esta entre comillas
print(f"El dato es: {dato_desconocido} y su tipo es: {type(dato_desconocido)}")

# Conversion (Casting): Transformando la caja de Texto a Numero (Integer)
dato_convertido = int(dato_desconocido)
print(f"Ahora el dato es: {dato_convertido} y su tipo es: {type(dato_convertido)}")

# Ahora si podemos hacer matemáticas
print(f"Suma matemática real: {dato_convertido + 50}")