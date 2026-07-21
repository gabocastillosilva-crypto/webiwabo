

import sys

from pathlib import Path



import pytest



sys.path.insert(0, str(Path(__file__).resolve().parents[2]))



from src.pago.pago import (

    Pago,

    PagoEfectivo,

    PagoTarjeta,

    PagoTransferencia,

)

from src.pago.procesador import (

    ProcesadorEfectivo,

    ProcesadorPago,

    ProcesadorTarjeta,

    ProcesadorTransferencia,

    crear_procesador,

)





def test_procesador_tarjeta_crea_pago_tarjeta():

    p = ProcesadorTarjeta("4111-1111-1111-1234").crear_pago()

    assert isinstance(p, PagoTarjeta)

    assert p.tipo() == "tarjeta"





def test_procesador_efectivo_crea_pago_efectivo():

    p = ProcesadorEfectivo().crear_pago()

    assert isinstance(p, PagoEfectivo)

    assert p.tipo() == "efectivo"





def test_procesador_transferencia_crea_pago_transferencia():

    p = ProcesadorTransferencia("GT123").crear_pago()

    assert isinstance(p, PagoTransferencia)

    assert p.tipo() == "transferencia"





def test_pagar_retorna_true(capsys):

    procesador = ProcesadorEfectivo()

    resultado = procesador.pagar(150.0)

    assert resultado is True





def test_pagar_muestra_tipo_correcto(capsys):

    ProcesadorTarjeta("4111-1111-1111-9999").pagar(50.0)

    assert "tarjeta" in capsys.readouterr().out





def test_nuevo_tipo_pago_no_modifica_base():

    class PagoCrypto(Pago):

        def procesar(self, monto):

            print(f"[CRYPTO] {monto} BTC")

            return True



        def tipo(self):

            return "crypto"



    class ProcesadorCrypto(ProcesadorPago):

        def crear_pago(self):

            return PagoCrypto()



    resultado = ProcesadorCrypto().pagar(0.005)

    assert resultado is True





def test_funcion_fabrica_efectivo():

    p = crear_procesador("efectivo")

    assert isinstance(p, ProcesadorEfectivo)





def test_funcion_fabrica_tipo_invalido():

    with pytest.raises(ValueError, match="Tipo de pago desconocido"):

        crear_procesador("cheque")

