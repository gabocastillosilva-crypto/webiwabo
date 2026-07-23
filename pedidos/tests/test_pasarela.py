import pytest

from src.pago.pago import PagoTarjeta, PagoEfectivo
from src.pago.factory import PasarelaPago, PasarelaProduccion, PasarelaPruebas, PagoMock


# ── Cada fábrica produce la familia correcta ──
def test_produccion_crea_tarjeta_real():
    pago = PasarelaProduccion().crear_pago_tarjeta("4111-0000-0000-0000")
    assert isinstance(pago, PagoTarjeta)


def test_produccion_crea_efectivo_real():
    pago = PasarelaProduccion().crear_pago_efectivo()
    assert isinstance(pago, PagoEfectivo)


def test_pruebas_crea_tarjeta_mock():
    pago = PasarelaPruebas().crear_pago_tarjeta("4111-0000-0000-0000")
    assert isinstance(pago, PagoMock)


def test_pruebas_crea_efectivo_mock():
    pago = PasarelaPruebas().crear_pago_efectivo()
    assert isinstance(pago, PagoMock)


# ── Las familias no se mezclan ──
def test_produccion_no_usa_mocks():
    fábrica = PasarelaProduccion()
    assert not isinstance(fábrica.crear_pago_tarjeta("0000"), PagoMock)
    assert not isinstance(fábrica.crear_pago_efectivo(), PagoMock)


def test_pruebas_no_usa_reales():
    fábrica = PasarelaPruebas()
    assert not isinstance(fábrica.crear_pago_tarjeta("0000"), PagoTarjeta)
    assert not isinstance(fábrica.crear_pago_efectivo(), PagoEfectivo)


# ── capsys: pruebas no hace cargos reales ──
def test_mock_no_menciona_banco(capsys):
    PasarelaPruebas().crear_pago_tarjeta("0000").procesar(100.0)
    salida = capsys.readouterr().out
    assert "[MOCK" in salida
    assert "TARJETA ****" not in salida  # no hay cargo real


# ── Fixture: inyección de fábrica ──
@pytest.fixture
def pasarela_pruebas():
    return PasarelaPruebas()


def test_con_fixture(pasarela_pruebas, capsys):
    pasarela_pruebas.crear_pago_efectivo().procesar(50.0)
    assert "[MOCK" in capsys.readouterr().out
