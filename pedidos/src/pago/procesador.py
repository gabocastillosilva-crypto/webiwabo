

from abc import ABC, abstractmethod



from src.pago.pago import Pago, PagoEfectivo, PagoTarjeta, PagoTransferencia





class ProcesadorPago(ABC):

    @abstractmethod

    def crear_pago(self) -> Pago:

        raise NotImplementedError



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

    if tipo == "tarjeta":

        return ProcesadorTarjeta(kwargs["numero"])

    if tipo == "efectivo":

        return ProcesadorEfectivo()

    if tipo == "transferencia":

        return ProcesadorTransferencia(kwargs["cuenta"])

    raise ValueError(f"Tipo de pago desconocido: '{tipo}'")

