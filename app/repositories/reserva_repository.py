"""
Repositorio de Reservas
"""

from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reserva import Reserva
from app.repositories.base_repository import BaseRepository


class ReservaRepository(BaseRepository[Reserva]):
    """
    Repositorio para la entidad Reserva
    """
    
    def __init__(self):
        super().__init__(Reserva)
    
    def get_by_cliente(self, db: Session, cliente_id: int) -> list[Reserva]:
        """Obtener reservas de un cliente"""
        return db.query(Reserva).filter(Reserva.cliente_id == cliente_id).all()
    
    def get_by_habitacion(self, db: Session, habitacion_id: int) -> list[Reserva]:
        """Obtener reservas de una habitación"""
        return db.query(Reserva).filter(Reserva.habitacion_id == habitacion_id).all()
    
    def get_by_estado(self, db: Session, estado: str) -> list[Reserva]:
        """Obtener reservas por estado"""
        return db.query(Reserva).filter(Reserva.estado == estado).all()
    
    def get_by_fechas(
        self,
        db: Session,
        fecha_inicio: date,
        fecha_fin: date
    ) -> list[Reserva]:
        """Obtener reservas en un rango de fechas"""
        return db.query(Reserva).filter(
            and_(
                Reserva.fecha_entrada >= fecha_inicio,
                Reserva.fecha_salida <= fecha_fin
            )
        ).all()
    
    def get_activas(self, db: Session) -> list[Reserva]:
        """Obtener reservas activas (pendientes o confirmadas)"""
        return db.query(Reserva).filter(
            Reserva.estado.in_(["pendiente", "confirmada"])
        ).all()
    
    def verificar_disponibilidad(
        self,
        db: Session,
        habitacion_id: int,
        fecha_entrada: date,
        fecha_salida: date,
        reserva_id: Optional[int] = None
    ) -> bool:
        """
        Verificar si una habitación está disponible en un rango de fechas
        """
        query = db.query(Reserva).filter(
            and_(
                Reserva.habitacion_id == habitacion_id,
                Reserva.estado.in_(["pendiente", "confirmada"]),
                # Conflicto de fechas
                (
                    (Reserva.fecha_entrada <= fecha_entrada) & (Reserva.fecha_salida > fecha_entrada) |
                    (Reserva.fecha_entrada < fecha_salida) & (Reserva.fecha_salida >= fecha_salida) |
                    (Reserva.fecha_entrada >= fecha_entrada) & (Reserva.fecha_salida <= fecha_salida)
                )
            )
        )
        
        # Excluir la reserva actual si estamos actualizando
        if reserva_id:
            query = query.filter(Reserva.id != reserva_id)
        
        return query.count() == 0


# Instancia singleton
reserva_repository = ReservaRepository()
