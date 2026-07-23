import pytest

from src.descuento.estrategias import (
    SinDescuento,
    DescuentoPorVolumen,
    DescuentoCupon,
    DescuentoVIP,
    EstrategiaDescuento,
)
from src.descuento.calculadora import CalculadoraDescuento


# ── Cada estrategia calcula correctamente ──
def test_sin_descuento():
    assert SinDescuento().calcular(100.0) == 0.0


def test_volumen_aplica_sobre_umbral():
    assert DescuentoPorVolumen().calcular(200.0) == 20.0


def test_volumen_no_aplica_bajo_umbral():
    assert DescuentoPorVolumen().calcular(50.0) == 0.0


def test_cupon_promo10():
    assert DescuentoCupon("PROMO10").calcular(100.0) == 10.0


def test_cupon_invalido_lanza_error():
    with pytest.raises(ValueError, match="inválido"):
        DescuentoCupon("CUPON_FALSO")


def test_vip_descuento_15_pct():
    assert DescuentoVIP().calcular(100.0) == 15.0


# ── La calculadora intercambia estrategias ──
def test_calculadora_sin_estrategia():
    calc = CalculadoraDescuento()
    resultado = calc.aplicar(100.0)
    assert resultado["total"] == 100.0


def test_calculadora_con_vip():
    calc = CalculadoraDescuento()
    calc.set_estrategia(DescuentoVIP())
    resultado = calc.aplicar(200.0)
    assert resultado["descuento"] == 30.0
    assert resultado["total"] == 170.0


def test_calculadora_cambio_de_estrategia_en_caliente():
    calc = CalculadoraDescuento()
    calc.set_estrategia(SinDescuento())
    assert calc.aplicar(100.0)["total"] == 100.0
    calc.set_estrategia(DescuentoVIP())
    assert calc.aplicar(100.0)["total"] == 85.0


# ── Principio Abierto/Cerrado: nueva estrategia sin modificar calculadora ──
def test_nueva_estrategia_no_modifica_calculadora():
    class DescuentoLanzamiento(EstrategiaDescuento):
        def calcular(self, subtotal):
            return subtotal * 0.25

        def descripcion(self):
            return "25% lanzamiento"

    calc = CalculadoraDescuento()
    calc.set_estrategia(DescuentoLanzamiento())
    assert calc.aplicar(100.0)["descuento"] == 25.0


# ── parametrize ──
@pytest.mark.parametrize(
    "estrategia,subtotal,esperado",
    [
        (SinDescuento(), 100.0, 0.0),
        (DescuentoPorVolumen(), 200.0, 20.0),
        (DescuentoPorVolumen(), 50.0, 0.0),
        (DescuentoVIP(), 100.0, 15.0),
    ],
)
def test_estrategias_parametrizadas(estrategia, subtotal, esperado):
    assert estrategia.calcular(subtotal) == esperado
