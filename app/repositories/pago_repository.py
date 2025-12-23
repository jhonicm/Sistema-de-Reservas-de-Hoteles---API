"""
Repositorio de Pagos
"""

from sqlalchemy.orm import Session
from app.models.pago import Pago
from app.repositories.base_repository import BaseRepository


class PagoRepository(BaseRepository[Pago]):
    """
    Repositorio para la entidad Pago
    """
    
    def __init__(self):
        super().__init__(Pago)
    
    def get_by_factura(self, db: Session, factura_id: int) -> list[Pago]:
        """Obtener pagos de una factura"""
        return db.query(Pago).filter(Pago.factura_id == factura_id).all()
    
    def get_total_pagado(self, db: Session, factura_id: int) -> float:
        """Calcular total pagado de una factura"""
        pagos = self.get_by_factura(db, factura_id)
        return sum(pago.monto for pago in pagos)


# Instancia singleton
pago_repository = PagoRepository()
