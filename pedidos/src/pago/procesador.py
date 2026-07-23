from abc import ABC, abstractmethod

from src.pago.pago import Pago, PagoTarjeta, PagoEfectivo, PagoTransferencia


class ProcesadorPago(ABC):
    @abstractmethod
    def crear_pago(self) -> Pago:
        pass

    
    def pagar(self, monto: float) -> bool:
        pago = self.crear_pago()
        print(f"Iniciando pago via {pago.tipo()}...")
        return pago.procesar(monto)


class ProcesadorTarjeta(ProcesadorPago):
    def __init__(self, numero: str):
        self._numero = numero

    def crear_pago(self) -> Pago:
         return PagoTarjeta(self._numero)
        



class ProcesadorEfectivo(ProcesadorPago):
    def crear_pago(self) -> Pago:
         return PagoEfectivo()
        


class ProcesadorTransferencia(ProcesadorPago):
    def __init__(self, cuenta: str):
        self._cuenta = cuenta

    def crear_pago(self) -> Pago:
         return PagoTransferencia(self._cuenta)
        


def crear_procesador(tipo: str, **kwargs) -> ProcesadorPago:
    """Función fábrica — alternativa simple sin jerarquía de Creator"""
    opciones = {
        "tarjeta": lambda: ProcesadorTarjeta(kwargs["numero"]),
        "efectivo": lambda: ProcesadorEfectivo(),
        "transferencia": lambda: ProcesadorTransferencia(kwargs["cuenta"]),
    }
    if tipo not in opciones:
        raise ValueError(f"Tipo de pago desconocido: '{tipo}'")
    return opciones[tipo]()
