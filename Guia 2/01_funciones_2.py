    # Exigimos estrictamente que 'nombre' y 'rol' sean de tipo String (str)
def crear_perfil(nombre: str, rol: str) -> None:
    """Registra un nuevo perfil en el sistema. """
    print(f"Registrando en base de datos: {nombre} | Permisos: {rol}")

# Si enviáramos crear_perfil(123, True), el editor nos marcaría una advertencia
crear_perfil("Carlos", "Admin")
crear_perfil("Ana", "Ventas")