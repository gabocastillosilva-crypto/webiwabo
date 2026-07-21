

from abc import ABC, abstractmethod





class Pago(ABC):

    @abstractmethod

    def procesar(self, monto: float) -> bool:

        raise NotImplementedError



    @abstractmethod

    def tipo(self) -> str:

        raise NotImplementedError





class PagoTarjeta(Pago):

    def __init__(self, numero: str):

        self._ultimos = numero[-4:] if numero else ""



    def procesar(self, monto: float) -> bool:

        return monto > 0



    def tipo(self) -> str:

        return "tarjeta"





class PagoEfectivo(Pago):

    def procesar(self, monto: float) -> bool:

        return monto > 0



    def tipo(self) -> str:

        return "efectivo"





class PagoTransferencia(Pago):

    def __init__(self, cuenta: str):

        self._cuenta = cuenta



    def procesar(self, monto: float) -> bool:

        return monto > 0



    def tipo(self) -> str:

        return "transferencia"

