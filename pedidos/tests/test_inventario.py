import pytest

from src.inventario.inventario import (
    FuenteInventario,
    SistemaInventarioLegacy,
    AdapterInventario,
)


# ── El Adapter implementa la interfaz Target ──
def test_adapter_es_fuente_inventario():
    adapter = AdapterInventario(SistemaInventarioLegacy())
    assert isinstance(adapter, FuenteInventario)


# ── El Adapter traduce disponible() → check_stock() ──
def test_disponible_retorna_bool(capsys):
    adapter = AdapterInventario(SistemaInventarioLegacy())
    resultado = adapter.disponible("Laptop")
    assert isinstance(resultado, bool)
    assert resultado is True


def test_disponible_convierte_nombre_a_sku(capsys):
    adapter = AdapterInventario(SistemaInventarioLegacy())
    adapter.disponible("Laptop")
    assert "LAP-001" in capsys.readouterr().out


# ── El Adapter traduce reservar() → reserve_item() ──
def test_reservar_retorna_bool():
    adapter = AdapterInventario(SistemaInventarioLegacy())
    assert adapter.reservar("Mouse", 2) is True


def test_reservar_convierte_nombre_a_sku(capsys):
    adapter = AdapterInventario(SistemaInventarioLegacy())
    adapter.reservar("Teclado", 1)
    assert "TEC-003" in capsys.readouterr().out


# ── El cliente usa FuenteInventario, no sabe que hay Legacy ──
def usar_inventario(fuente: FuenteInventario, producto: str) -> bool:
    """Función cliente — solo conoce FuenteInventario"""
    if fuente.disponible(producto):
        return fuente.reservar(producto, 1)
    return False


def test_cliente_independiente_del_legacy():
    adapter = AdapterInventario(SistemaInventarioLegacy())

    resultado = usar_inventario(adapter, "Monitor")
    assert resultado is True
