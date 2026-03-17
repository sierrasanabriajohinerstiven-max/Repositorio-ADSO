# 1. EL MOLDE: Definimos la clase (Siempre inicia en Mayúscula)
class Mascota:

    # 2. CONSTRUCTOR: Se ejecuta automáticamente al crear el objeto
    def __init__(self, nombre: str, tipo: str, edad: int):

        # 3. ATRIBUTOS: Características propias de cada mascota
        self.nombre: str = nombre
        self.tipo: str = tipo
        self.edad: int = edad
        self.estado: str = "Descansando"  # Estado inicial por defecto

    # 4. MÉTODOS: Acciones que puede realizar la mascota
    def saludar(self):
        print(f"Hola, soy {self.nombre} y soy un {self.tipo}")

    def comer(self):
        self.estado = "Comiendo"
        print(f"{self.nombre} ahora está comiendo.")

    def dormir(self):
        self.estado = "Durmiendo"
        print(f"{self.nombre} se fue a dormir")


# 5. INSTANCIACIÓN: Creando objetos en memoria
mascota1 = Mascota("Max", "Perro", 3)
mascota2 = Mascota("Michi", "Gato", 2)


# 6. USANDO LOS MÉTODOS
mascota1.saludar()
mascota1.comer()
print(f"Estado actual de {mascota1.nombre}: {mascota1.estado}")

mascota2.saludar()
mascota2.dormir()
print(f"Estado actual de {mascota2.nombre}: {mascota2.estado}")