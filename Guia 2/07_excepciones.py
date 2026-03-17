class CajeroAutomatico:

    def __init__(self):
        self.efectivo_disponible: float = 10000.0

    def solicitar_retiro(self) -> None:
        print("\n--- Bienvenido al Cajero ---")

        # Bloque TRY: "Intenta hacer esto, pero estate alerta"
        try:
            monto_str: str = input("Ingrese la cantidad a retirar (solo números): ")

            # Si el usuario ingresa letras, esta conversión generará un ValueError
            monto: float = float(monto_str)

            # Si el usuario ingresa cero, lanzamos nuestra propia excepción lógica
            if monto == 0:
                raise ValueError("No puede retirar cero pesos.")

            # Validar fondos suficientes
            if monto > self.efectivo_disponible:
                raise ValueError("Fondos insuficientes.")

            # Operación matemática
            self.efectivo_disponible -= monto

            print(f"Retiro exitoso. Quedan ${self.efectivo_disponible} en el cajero.")

        # Bloque EXCEPT: Manejo de errores específicos
        except ValueError as e:
            print(f"⚠ ERROR: Entrada inválida o problema lógico. ({e})")

        # Captura cualquier otro error inesperado
        except Exception as e:
            print(f"🚨 ERROR CRÍTICO DESCONOCIDO: Contacte soporte. Detalles: {e}")

        # Bloque FINALLY: Se ejecuta SIEMPRE
        finally:
            print("Expulsando tarjeta... Gracias por utilizar nuestra red.\n")


# Prueba
mi_cajero = CajeroAutomatico()

# Intenta ingresar letras como "Hola" o números grandes para probar el sistema
mi_cajero.solicitar_retiro()