"""
Repositorio de Habitaciones
"""

from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from app.models.habitacion import Habitacion
from app.models.reserva import Reserva
from app.repositories.base_repository import BaseRepository


class HabitacionRepository(BaseRepository[Habitacion]):
    """
    Repositorio para la entidad Habitación
    """
    
    def __init__(self):
        super().__init__(Habitacion)
    
    def get_by_numero(self, db: Session, numero: str) -> Optional[Habitacion]:
        """Buscar habitación por número"""
        return db.query(Habitacion).filter(Habitacion.numero == numero).first()
    
    def get_by_tipo(self, db: Session, tipo: str) -> list[Habitacion]:
        """Obtener habitaciones por tipo"""
        return db.query(Habitacion).filter(Habitacion.tipo == tipo).all()
    
    def get_disponibles(self, db: Session, tipo: Optional[str] = None) -> list[Habitacion]:
        """Obtener habitaciones disponibles"""
        query = db.query(Habitacion).filter(
            and_(
                Habitacion.estado == "Disponible",
                Habitacion.activa == True
            )
        )
        
        if tipo:
            query = query.filter(Habitacion.tipo == tipo)
        
        return query.all()
    
    def get_disponibles_por_fechas(
        self,
        db: Session,
        fecha_entrada: date,
        fecha_salida: date,
        tipo: Optional[str] = None
    ) -> list[Habitacion]:
        """
        Obtener habitaciones disponibles en un rango de fechas
        """
        # Subconsulta para habitaciones reservadas en las fechas
        habitaciones_reservadas = db.query(Reserva.habitacion_id).filter(
            and_(
                Reserva.estado.in_(["pendiente", "confirmada"]),
                or_(
                    and_(
                        Reserva.fecha_entrada <= fecha_entrada,
                        Reserva.fecha_salida > fecha_entrada
                    ),
                    and_(
                        Reserva.fecha_entrada < fecha_salida,
                        Reserva.fecha_salida >= fecha_salida
                    ),
                    and_(
                        Reserva.fecha_entrada >= fecha_entrada,
                        Reserva.fecha_salida <= fecha_salida
                    )
                )
            )
        ).subquery()
        
        # Consulta de habitaciones disponibles
        query = db.query(Habitacion).filter(
            and_(
                Habitacion.activa == True,
                Habitacion.estado == "disponible",
                not_(Habitacion.id.in_(habitaciones_reservadas))
            )
        )
        
        if tipo:
            query = query.filter(Habitacion.tipo == tipo)
        
        return query.all()


# Instancia singleton
habitacion_repository = HabitacionRepository()
