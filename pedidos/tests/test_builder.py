

import sys

from pathlib import Path



import pytest



sys.path.insert(0, str(Path(__file__).resolve().parents[1]))



from src.pedido.builder import PedidoBuilder

from src.pedido.pedido import Pedido





def test_builder_crea_pedido():

    pedido = (

        PedidoBuilder()

        .para("Ana López")

        .agregar_item("Laptop", 899.99)

        .construir()

    )

    assert isinstance(pedido, Pedido)





def test_builder_fluent_retorna_self():

    b = PedidoBuilder()

    assert b.para("Ana") is b

    assert b.agregar_item("X", 10.0) is b

    assert b.enviar_a("Calle 1") is b

    assert b.con_descuento(0.1) is b





def test_builder_calcula_total_con_descuento():

    pedido = (

        PedidoBuilder()

        .para("Carlos")

        .agregar_item("Mouse", 25.00)

        .agregar_item("Teclado", 75.00)

        .con_descuento(0.10)

        .construir()

    )

    assert pedido.subtotal == 100.00

    assert pedido.total == 90.00





def test_builder_multiples_items():

    pedido = (

        PedidoBuilder()

        .para("María")

        .agregar_item("Monitor", 300.00, 2)

        .construir()

    )

    assert pedido.subtotal == 600.00





def test_builder_sin_cliente_lanza_error():

    with pytest.raises(ValueError, match="cliente"):

        PedidoBuilder().agregar_item("X", 1.0).construir()





def test_builder_sin_items_lanza_error():

    with pytest.raises(ValueError, match="ítem"):

        PedidoBuilder().para("Ana").construir()





def test_builder_descuento_invalido_lanza_error():

    with pytest.raises(ValueError):

        PedidoBuilder().para("Ana").con_descuento(1.5)





def test_pedido_tiene_numero_unico():

    p1 = PedidoBuilder().para("A").agregar_item("X", 1.0).construir()

    p2 = PedidoBuilder().para("B").agregar_item("Y", 2.0).construir()

    assert p1.numero != p2.numero

