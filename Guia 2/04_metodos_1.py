class CuentaBancaria:
    def __init__(self, titular: str, saldo_inicial: float):
        self.titular: str = titular
        self.saldo: float = saldo_inicial

# MÉTODO: Una acción. Nota cómo recibe 'self' y luego los parámetros útiles.
def depositar(self, cantidad: float) -> None:
    self.saldo += cantidad
    print(f"Depósito exitoso. Nuevo saldo de {self.titular}: ${self.saldo}")

def retirar(self, cantidad: float) -> None:
    if cantidad > self.saldo:
        print(f"X Error: {self.titular} no tiene fondos suficientes.")
    else:
        self.saldo -= cantidad
        print(f"o Retiro exitoso. Saldo restante: ${self.saldo}")

# Creando y manipulando objetos
cuenta_ana = CuentaBancaria("Ana López", 50000.0)

cuenta_ana.depositar(20000.0)
cuenta_ana.retirar(100000.0) # Deberia arrojar el error de fondos
cuenta_ana.retirar(15000.0)
