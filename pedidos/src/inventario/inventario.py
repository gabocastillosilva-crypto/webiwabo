from abc import ABC, abstractmethod


# ── Target: lo que el sistema espera ──────────────────────
class FuenteInventario(ABC):
    @abstractmethod
    def disponible(self, producto: str) -> bool:
        pass

    @abstractmethod
    def reservar(self, producto: str, cantidad: int) -> bool:
        pass


# ── Adaptee: sistema legado — NO modificar ────────────────
class SistemaInventarioLegacy:
    def check_stock(self, sku: str, qty: int) -> str:
        """Retorna 'OK' si hay stock, 'NO_STOCK' si no"""
        print(f"[LEGACY] check_stock(sku={sku}, qty={qty})")
        return "OK"  # simplificado — en prod consultaría la BD

    def reserve_item(self, sku: str, qty: int) -> bool:
        print(f"[LEGACY] reserve_item(sku={sku}, qty={qty})")
        return True


# ── Adapter ────────────────────────────────────────────────
class AdapterInventario(FuenteInventario):
    SKU_MAP = {
        "Laptop": "LAP-001",
        "Mouse": "MOU-002",
        "Teclado": "TEC-003",
        "Monitor": "MON-004",
    }

    def __init__(self, sistema: SistemaInventarioLegacy):
        self._sistema = sistema

    def _a_sku(self, producto: str) -> str:
        return self.SKU_MAP.get(producto, producto.upper().replace(" ", "-"))

    def disponible(self, producto: str) -> bool:
        sku = self._a_sku(producto)
        return self._sistema.check_stock(sku, 1) == "OK"
        

    def reservar(self, producto: str, cantidad: int) -> bool:
        sku = self._a_sku(producto)
        return self._sistema.reserve_item(sku, cantidad)
        
