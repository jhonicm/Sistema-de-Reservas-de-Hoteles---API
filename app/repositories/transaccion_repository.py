"""
Repositorio de Transacciones Contables
"""

from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.transaccion import Transaccion
from app.repositories.base_repository import BaseRepository


class TransaccionRepository(BaseRepository[Transaccion]):
    """
    Repositorio para la entidad Transacción
    """
    
    def __init__(self):
        super().__init__(Transaccion)
    
    def get_by_cuenta(self, db: Session, cuenta_id: int) -> list[Transaccion]:
        """Obtener transacciones de una cuenta"""
        return db.query(Transaccion).filter(Transaccion.cuenta_id == cuenta_id).all()
    
    def get_by_tipo(self, db: Session, tipo: str) -> list[Transaccion]:
        """Obtener transacciones por tipo (ingreso/egreso)"""
        return db.query(Transaccion).filter(Transaccion.tipo == tipo).all()
    
    def get_by_fecha_rango(
        self,
        db: Session,
        fecha_inicio: date,
        fecha_fin: date
    ) -> list[Transaccion]:
        """Obtener transacciones en un rango de fechas"""
        return db.query(Transaccion).filter(
            and_(
                Transaccion.fecha_transaccion >= fecha_inicio,
                Transaccion.fecha_transaccion <= fecha_fin
            )
        ).all()
    
    def get_total_ingresos(self, db: Session, fecha_inicio: date, fecha_fin: date) -> float:
        """Calcular total de ingresos en un período"""
        result = db.query(func.sum(Transaccion.monto)).filter(
            and_(
                Transaccion.tipo == "ingreso",
                Transaccion.fecha_transaccion >= fecha_inicio,
                Transaccion.fecha_transaccion <= fecha_fin
            )
        ).scalar()
        return result if result else 0.0
    
    def get_total_egresos(self, db: Session, fecha_inicio: date, fecha_fin: date) -> float:
        """Calcular total de egresos en un período"""
        result = db.query(func.sum(Transaccion.monto)).filter(
            and_(
                Transaccion.tipo == "egreso",
                Transaccion.fecha_transaccion >= fecha_inicio,
                Transaccion.fecha_transaccion <= fecha_fin
            )
        ).scalar()
        return result if result else 0.0


# Instancia singleton
transaccion_repository = TransaccionRepository()
