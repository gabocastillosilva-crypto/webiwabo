from src.descuento.estrategias import EstrategiaDescuento, SinDescuento


class CalculadoraDescuento:
    def __init__(self):
        self._estrategia: EstrategiaDescuento = SinDescuento()

    def set_estrategia(self, estrategia: EstrategiaDescuento):
        self._estrategia = estrategia

    def aplicar(self, subtotal: float) -> dict:
        descuento = self._estrategia.calcular(subtotal)
        return {
            "subtotal": subtotal,
            "descuento": descuento,
            "total": subtotal - descuento,
            "descripcion": self._estrategia.descripcion(),
        }
