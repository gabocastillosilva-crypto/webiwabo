from src.config.configuracion import ConfiguracionApp
from src.pedido.builder import PedidoBuilder
from src.pedido.gestor import GestorPedidos
from src.pedido.observadores import NotificadorCliente, RegistroAuditoria
from src.pago.factory import obtener_pasarela
from src.inventario.inventario import AdapterInventario, SistemaInventarioLegacy
from src.notificacion.canales import CanalEmail, CanalSMS
from src.notificacion.notificaciones import NotificacionPedido
from src.descuento.estrategias import DescuentoPorVolumen
from src.descuento.calculadora import CalculadoraDescuento


def main():
    # ── Singleton: configuración global ──────────────────
    config = ConfiguracionApp()
    print(f"\n{'='*50}")
    print(f"Sistema iniciado — {config}")
    print(f"{'='*50}\n")

    # ── Builder: construir el pedido ──────────────────────
    pedido = (
        PedidoBuilder()
        .para("Ana López")
        .agregar_item("Laptop", 899.99)
        .agregar_item("Mouse", 25.00)
        .agregar_item("Teclado", 75.00)
        .enviar_a("Av. Principal 123, Ciudad")
        .con_notas("Entregar en horario de oficina")
        .construir()
    )
    print(f"Pedido creado:\n{pedido}\n")

    # ── Strategy: calcular descuento ──────────────────────
    calc = CalculadoraDescuento()
    calc.set_estrategia(DescuentoPorVolumen())
    resultado = calc.aplicar(pedido.subtotal)
    print(f"Descuento aplicado: {resultado['descripcion']}")
    print(f"Total final: ${resultado['total']:.2f}\n")

    # ── Abstract Factory: pasarela según entorno ──────────
    pasarela = obtener_pasarela()
    pago = pasarela.crear_pago_tarjeta("4111-1111-1111-1234")
    aprobado = pago.procesar(resultado["total"])
    print(f"Pago aprobado: {aprobado}\n")

    # ── Adapter: verificar inventario ────────────────────
    inventario = AdapterInventario(SistemaInventarioLegacy())
    for item, _, _ in pedido.items:
        disp = inventario.disponible(item)
        print(f" Stock '{item}': {'✓' if disp else '✗'}")
        if disp:
            inventario.reservar(item, 1)
    print()

    # ── Observer: gestionar estados ───────────────────────
    gestor = GestorPedidos()
    gestor.suscribir(NotificadorCliente())
    gestor.suscribir(RegistroAuditoria())
    gestor.registrar(pedido.numero)
    gestor.cambiar_estado(pedido.numero, "confirmado")
    gestor.cambiar_estado(pedido.numero, "enviado")
    print()

    # ── Bridge: notificar por canal ───────────────────────
    notif_email = NotificacionPedido(CanalEmail(), pedido.numero, "enviado")
    notif_sms = NotificacionPedido(CanalSMS(), pedido.numero, "enviado")
    notif_email.enviar("ana@email.com")
    notif_sms.enviar("+52555123456")


if __name__ == "__main__":
    main()