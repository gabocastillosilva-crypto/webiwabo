

class Pedido:

    def __init__(self):

        self.cliente = ""

        self.items = []

        self.direccion = ""

        self.descuento = 0.0

        self.notas = ""

        self.estado = "pendiente"

        self.numero = ""



    @property

    def subtotal(self) -> float:

        return sum(precio * cantidad for _, precio, cantidad in self.items)



    @property

    def total(self) -> float:

        return self.subtotal * (1 - self.descuento)



    def __str__(self):

        lineas = "\n ".join(

            f"{nombre}: ${precio:.2f} x{cantidad}"

            for nombre, precio, cantidad in self.items

        )

        return (

            f"Pedido #{self.numero} — {self.cliente}\n"

            f" {lineas}\n"

            f" Dirección: {self.direccion}\n"

            f" Descuento: {self.descuento * 100:.0f}%\n"

            f" Total: ${self.total:.2f}\n"

            f" Estado: {self.estado}"

        )

