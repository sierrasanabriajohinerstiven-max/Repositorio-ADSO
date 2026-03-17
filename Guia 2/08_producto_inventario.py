# 1. CLASE BASE: Producto
class Producto:

    # Constructor que recibe nombre, precio y stock
    def __init__(self, nombre: str, precio: float, stock: int):
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    # Método vender con manejo de errores (Resiliencia)
    def vender(self, cantidad: int) -> None:
        print(f"\nIntentando vender {cantidad} unidad(es) de {self.nombre}...")

        try:
            # Validar si hay suficiente stock
            if cantidad > self.stock:
                raise ValueError("Stock insuficiente")

            # Si pasa la validación, se descuenta del inventario
            self.stock -= cantidad
            total: float = cantidad * self.precio

            print(f"Venta exitosa ✅")
            print(f"Total a pagar: ${total}")
            print(f"Stock restante: {self.stock}")

        except ValueError as e:
            print(f"⚠ ERROR: {e}")
            print("No se pudo completar la venta, pero el sistema sigue funcionando.")


# 2. CLASE HEREDADA: ProductoPerecedero
class ProductoPerecedero(Producto):

    # Hereda nombre, precio y stock del padre
    # Agrega dias_vencimiento
    def __init__(self, nombre: str, precio: float, stock: int, dias_vencimiento: int):
        super().__init__(nombre, precio, stock)
        self.dias_vencimiento: int = dias_vencimiento


# ==========================================================
# PRUEBAS DEL SISTEMA (Simulación)
# ==========================================================

# Producto normal
arroz = Producto("Arroz", 2500.0, 10)

# Producto perecedero
leche = ProductoPerecedero("Leche", 3000.0, 5, 7)

# Venta exitosa
arroz.vender(3)

# Venta fallida por falta de stock
arroz.vender(20)

# Venta exitosa producto perecedero
leche.vender(2)

# Venta fallida producto perecedero
leche.vender(10)