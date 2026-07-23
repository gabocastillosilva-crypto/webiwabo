import pytest

from src.pedido.gestor import GestorPedidos
from src.pedido.observadores import (
    NotificadorCliente,
    RegistroAuditoria,
    ActualizadorInventario,
)


@pytest.fixture
def gestor():
    return GestorPedidos()


# ── El gestor notifica a todos los suscriptores ──
def test_registrar_pedido_notifica_observadores(gestor, capsys):
    gestor.suscribir(NotificadorCliente())
    gestor.registrar("P001")
    assert "P001" in capsys.readouterr().out


def test_cambiar_estado_notifica(gestor, capsys):
    gestor.suscribir(NotificadorCliente())
    gestor.registrar("P002")
    gestor.cambiar_estado("P002", "enviado")
    assert "enviado" in capsys.readouterr().out


# ── El historial de auditoría se actualiza ──
def test_auditoria_registra_cambios(gestor):
    auditoria = RegistroAuditoria()
    gestor.suscribir(auditoria)
    gestor.registrar("P003")
    gestor.cambiar_estado("P003", "confirmado")
    gestor.cambiar_estado("P003", "enviado")
    assert len(auditoria.historial) == 3
    assert "enviado" in auditoria.historial[-1]


# ── El inventario solo reacciona al estado "enviado" ──
def test_inventario_solo_reacciona_a_enviado(gestor, capsys):
    gestor.suscribir(ActualizadorInventario())
    gestor.registrar("P004")
    gestor.cambiar_estado("P004", "confirmado")
    gestor.cambiar_estado("P004", "enviado")
    salida = capsys.readouterr().out
    assert salida.count("[INVENTARIO]") == 1


# ── Se puede desuscribir un observador ──
def test_desuscribir_observador(gestor, capsys):
    notif = NotificadorCliente()
    gestor.suscribir(notif)
    gestor.registrar("P005")
    gestor.desuscribir(notif)
    gestor.cambiar_estado("P005", "enviado")
    salida = capsys.readouterr().out
    # Solo debe aparecer el primer estado (registro), no el "enviado"
    assert "enviado" not in salida


# ── Pedido no registrado lanza error ──
def test_cambiar_estado_pedido_inexistente(gestor):
    with pytest.raises(KeyError):
        gestor.cambiar_estado("NO_EXISTE", "enviado")
