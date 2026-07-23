from src.pedido.observadores import ObservadorPedido


class GestorPedidos:
    def __init__(self):
        self._observadores: list[ObservadorPedido] = []
        self._pedidos: dict[str, str] = {}

    def suscribir(self, obs: ObservadorPedido):
        self._observadores.append(obs)

    def desuscribir(self, obs: ObservadorPedido):
        self._observadores.remove(obs)

    def _notificar(self, numero: str, estado: str):
         for obs in self._observadores:
          obs.actualizar(numero, estado)
        

    def registrar(self, numero: str):
        self._pedidos[numero] = "pendiente"
        self._notificar(numero, "pendiente")

    def cambiar_estado(self, numero: str, nuevo_estado: str):
         if numero not in self._pedidos:
          raise KeyError(f"Pedido '{numero}' no encontrado")
         self._pedidos[numero] = nuevo_estado
         self._notificar(numero, nuevo_estado)

    def estado(self, numero: str) -> str:
        return self._pedidos.get(numero, "no encontrado")
