from abc import ABC, abstractmethod


class Pago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> bool:
        pass

    @abstractmethod
    def tipo(self) -> str:
        pass


class PagoTarjeta(Pago):
    def __init__(self, numero: str):
        self._ultimos = numero[-4:]

    def procesar(self, monto: float) -> bool:
         print(f"[TARJETA ****{self._ultimos}] Procesando ${monto:.2f}")
         return True
        

    def tipo(self):
        return "tarjeta"


class PagoEfectivo(Pago):
    def procesar(self, monto: float) -> bool:
         print(f"[EFECTIVO] Registrando ${monto:.2f}")
         return True
        

    def tipo(self):
        return "efectivo"


class PagoTransferencia(Pago):
    def __init__(self, cuenta: str):
        self._cuenta = cuenta

    def procesar(self, monto: float) -> bool:
         print(f"[TRANSFERENCIA → {self._cuenta}] ${monto:.2f}")
         return True
        

    def tipo(self):
        return "transferencia"
