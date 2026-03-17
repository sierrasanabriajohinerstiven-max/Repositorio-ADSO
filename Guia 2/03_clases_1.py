# 1. EL MOLDE: La Clase (Por convención, empieza con Mayúscula)
class Servidor:

    # 2. EL CONSTRUCTOR: Se ejecuta automáticamente al instanciar.
    def __init__(self, nombre: str, ip: str, ram_gb: int):

        # 3. ATRIBUTOS: Variables que le pertenecen solo a este objeto en la RAM
        self.nombre: str = nombre
        self.ip: str = ip
        self.ram: int = ram_gb
        self.estado: str = "Apagado"  # Valor inicial por defecto

# 4. INSTANCIACIÓN: Construyendo los objetos físicos en RAM
server_ventas = Servidor("Ventas-01", "192.168.1.10", 16)
server_bd = Servidor("Database-Main", "10.0.0.5", 64)

# 5. Accediendo a la información específica usando el puntero del objeto
print(f"El servidor {server_ventas.nombre} tiene {server_ventas.ram}GB de RAM.")
print(f"El servidor {server_bd.nombre} actualmente está: {server_bd.estado}")





