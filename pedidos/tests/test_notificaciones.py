import pytest
from src.notificacion.canales import CanalEmail, CanalSMS, CanalConsola
from src.notificacion.notificaciones import NotificacionPedido, AlertaStock


def test_notif_pedido_por_email(capsys):
    NotificacionPedido(CanalEmail(), "ABC123", "enviado").enviar("ana@mail.com")
    assert "[EMAIL → ana@mail.com]" in capsys.readouterr().out


def test_notif_pedido_por_sms(capsys):
    NotificacionPedido(CanalSMS(), "ABC123", "enviado").enviar("+52555")
    assert "[SMS → +52555]" in capsys.readouterr().out


def test_alerta_stock_por_email(capsys):
    AlertaStock(CanalEmail(), "Laptop", 3).enviar("admin@tienda.com")
    salida = capsys.readouterr().out
    assert "Laptop" in salida
    assert "[EMAIL →" in salida


def test_cambiar_canal_en_caliente(capsys):
    notif = NotificacionPedido(CanalEmail(), "XYZ", "pendiente")
    notif.enviar("cliente@mail.com")
    notif.cambiar_canal(CanalSMS())
    notif.enviar("+52555")

    salida = capsys.readouterr().out
    assert "[EMAIL →" in salida
    assert "[SMS →" in salida


def test_nuevo_canal_no_modifica_notificaciones(capsys):
    from src.notificacion.canales import Canal

    class CanalWhatsApp(Canal):
        def enviar(self, dest, texto):
            print(f"[WA → {dest}] {texto}")

    AlertaStock(CanalWhatsApp(), "Mouse", 1).enviar("+52555")
    assert "[WA →" in capsys.readouterr().out


@pytest.mark.parametrize("canal_cls", [CanalEmail, CanalSMS, CanalConsola])
def test_alerta_funciona_con_todos_los_canales(canal_cls, capsys):
    AlertaStock(canal_cls(), "Teclado", 5).enviar("dest")
    salida = capsys.readouterr().out
    assert "Teclado" in salida
    assert "5 unidades" in salida

