





import os





class ConfiguracionApp:

    _instancia = None



    def __new__(cls):

        if cls._instancia is None:

            cls._instancia = super().__new__(cls)

            cls._instancia.entorno = os.getenv("ENTORNO", "produccion")

            cls._instancia.version = "1.0.0"

            cls._instancia.debug = os.getenv("DEBUG", "false").lower() == "true"

        return cls._instancia



    def es_produccion(self) -> bool:

        return self.entorno == "produccion"



    def __str__(self):

        return f"Config(entorno={self.entorno}, version={self.version}, debug={self.debug})"
