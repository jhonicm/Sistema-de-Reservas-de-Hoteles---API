"""
Modelo de Reserva
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Reserva(Base):
    """
    Entidad Reserva - Gestión de reservas del hotel
    """
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Relaciones foráneas
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    habitacion_id = Column(Integer, ForeignKey("habitaciones.id"), nullable=False)
    
    # Fechas
    fecha_entrada = Column(Date, nullable=False)
    fecha_salida = Column(Date, nullable=False)
    
    # Información financiera
    precio_total = Column(Float, nullable=False)
    
    # Estado
    estado = Column(String(20), default="pendiente", nullable=False)  
    # Estados: pendiente, confirmada, cancelada, completada
    
    # Observaciones
    observaciones = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="reservas")
    habitacion = relationship("Habitacion", back_populates="reservas")
    factura = relationship("Factura", back_populates="reserva", uselist=False)
    
    # Restricciones
    __table_args__ = (
        CheckConstraint('fecha_salida > fecha_entrada', name='check_fechas_validas'),
    )
    
    def __repr__(self):
        return f"<Reserva #{self.id} - Cliente:{self.cliente_id} - Habitación:{self.habitacion_id} - {self.estado}>"
