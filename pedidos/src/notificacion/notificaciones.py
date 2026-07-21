from abc import ABC, abstractmethod

from src.notificacion.canales import Canal


class Notificacion(ABC):
    def __init__(self, canal: Canal):
        self._canal = canal  # ← el puente

    @abstractmethod
    def enviar(self, destinatario: str) -> None:
        pass

    def cambiar_canal(self, canal: Canal):
        """Intercambio en caliente — imposible con herencia."""
        self._canal = canal


class NotificacionPedido(Notificacion):
    def __init__(self, canal: Canal, numero: str, estado: str):
        super().__init__(canal)
        self._numero = numero
        self._estado = estado

    def enviar(self, destinatario: str) -> None:
        self._canal.enviar(
            destinatario,
            f"Pedido #{self._numero} → Estado: {self._estado}",
        )


class AlertaStock(Notificacion):
    def __init__(self, canal: Canal, producto: str, unidades: int):
        super().__init__(canal)
        self._producto = producto
        self._unidades = unidades

    def enviar(self, destinatario: str) -> None:
        self._canal.enviar(
            destinatario,
            f"⚠ Stock bajo — {self._producto}: {self._unidades} unidades",
        )
