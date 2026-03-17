# 1. Definición: '-> None' indica que esta función no devuelve datos a la memoria
def saludar_usuario() -> None:
    """Imprime un mensaje de conexión estándar. """
    print("Iniciando conexión con el servidor ... ")
    print("Autenticación exitosa. ¡Bienvenido!")

# 2. Llamada (La ejecución): Pedirle a la función que haga su trabajo
print(" --- Sistema Principal --- ")
saludar_usuario()
saludar_usuario()

print(" --- Fin del Sistema --- ")