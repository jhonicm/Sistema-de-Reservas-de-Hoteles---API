"""
Modelo de Cliente
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Cliente(Base):
    """
    Entidad Cliente - Gestión de clientes del hotel
    """
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Información personal
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    identificacion = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reservas = relationship("Reserva", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente {self.nombre} {self.apellido} - {self.identificacion}>"
