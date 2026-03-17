#Creo la clase vehiculo
class Vehiculo:
    def __init__(self, marca: str, modelo: str, anio: int, precio: float, color: str):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.precio = precio
        self.color = color

    def __str__(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Año: {self.anio}, Precio: {self.precio}, Color: {self.color}"

#Imprimo los datos del vehiculo
vehiculo = Vehiculo("Toyota", "Corolla", 2022, 15000000, "Azul")
print(vehiculo)
