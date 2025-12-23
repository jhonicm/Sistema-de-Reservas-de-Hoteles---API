"""
Repositorio de Facturas
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.repositories.base_repository import BaseRepository


class FacturaRepository(BaseRepository[Factura]):
    """
    Repositorio para la entidad Factura
    """
    
    def __init__(self):
        super().__init__(Factura)
    
    def get_by_numero(self, db: Session, numero_factura: str) -> Optional[Factura]:
        """Buscar factura por número"""
        return db.query(Factura).filter(Factura.numero_factura == numero_factura).first()
    
    def get_by_reserva(self, db: Session, reserva_id: int) -> Optional[Factura]:
        """Obtener factura de una reserva"""
        return db.query(Factura).filter(Factura.reserva_id == reserva_id).first()
    
    def get_ultimo_numero(self, db: Session) -> str:
        """Obtener el último número de factura para generar el siguiente"""
        ultima_factura = db.query(Factura).order_by(Factura.id.desc()).first()
        if ultima_factura:
            return ultima_factura.numero_factura
        return "FAC-0000"


# Instancia singleton
factura_repository = FacturaRepository()
