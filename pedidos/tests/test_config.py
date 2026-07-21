

import sys

from pathlib import Path



sys.path.insert(0, str(Path(__file__).resolve().parents[1]))



from src.config.configuracion import ConfiguracionApp





def test_singleton_retorna_misma_instancia():

    a = ConfiguracionApp()

    b = ConfiguracionApp()

    assert a is b





def test_singleton_mismos_valores():

    a = ConfiguracionApp()

    b = ConfiguracionApp()

    assert a.version == b.version

    assert a.entorno == b.entorno





def test_configuracion_tiene_version():

    config = ConfiguracionApp()

    assert config.version == "1.0.0"





def test_es_produccion_por_defecto():

    config = ConfiguracionApp()

    assert config.es_produccion() is (config.entorno == "produccion")

