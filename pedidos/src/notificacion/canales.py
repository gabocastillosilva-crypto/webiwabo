from abc import ABC, abstractmethod


class Canal(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, texto: str) -> None:
        pass


class CanalEmail(Canal):
    def enviar(self, destinatario, texto):
         print(f"[EMAIL → {destinatario}] {texto}")
        


class CanalSMS(Canal):
    def enviar(self, destinatario, texto):
         print(f"[SMS → {destinatario}] {texto}")
        


class CanalConsola(Canal):
    """Útil para pruebas y logging interno"""

    def enviar(self, destinatario, texto):
         print(f"[LOG] {destinatario}: {texto}")
        
