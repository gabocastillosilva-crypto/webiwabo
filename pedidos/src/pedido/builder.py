import uuid

from src.pedido.pedido import Pedido


class PedidoBuilder:
    def __init__(self):
        self._pedido = Pedido()

    def para(self, cliente: str):
         self._pedido.cliente = cliente
         return self

    def agregar_item(self, nombre: str, precio: float, cantidad: int = 1):
         self._pedido.items.append((nombre, precio, cantidad))
         return self

    def enviar_a(self, direccion: str):
         self._pedido.direccion = direccion
         return self

    def con_descuento(self, porcentaje: float):
        """porcentaje entre 0.0 y 1.0 (ej. 0.10 = 10%)"""
        if not 0.0 <= porcentaje <= 1.0:
            raise ValueError("El descuento debe estar entre 0.0 y 1.0")
        self._pedido.descuento = porcentaje
        return self

    def con_notas(self, notas: str):
        self._pedido.notas = notas
        return self

    def construir(self) -> Pedido:
         if not self._pedido.cliente:
            raise ValueError("El pedido debe tener un cliente")
         if not self._pedido.items:
            raise ValueError("El pedido debe tener al menos un ítem")
         self._pedido.numero = str(uuid.uuid4())[:8].upper()
         return self._pedido
