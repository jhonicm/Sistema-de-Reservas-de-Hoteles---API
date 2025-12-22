"""
Modelo de Habitación
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Habitacion(Base):
    """
    Entidad Habitación - Gestión de habitaciones del hotel
    """
    __tablename__ = "habitaciones"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Información de la habitación
    numero = Column(String(10), unique=True, nullable=False, index=True)
    tipo = Column(String(50), nullable=False)  # Simple, Doble, Suite, etc.
    precio_noche = Column(Float, nullable=False)
    capacidad = Column(Integer, nullable=False)
    
    # Características
    caracteristicas = Column(Text, nullable=True)  # JSON o texto con características
    
    # Estado
    estado = Column(String(20), default="disponible", nullable=False)  # disponible, ocupada, mantenimiento
    activa = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reservas = relationship("Reserva", back_populates="habitacion")
    
    def __repr__(self):
        return f"<Habitacion {self.numero} - {self.tipo} - {self.estado}>"
