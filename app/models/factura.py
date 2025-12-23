"""
Modelo de Factura
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Factura(Base):
    """
    Entidad Factura - Gestión de facturas
    """
    __tablename__ = "facturas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Número de factura único
    numero_factura = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relación con reserva
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False)
    
    # Montos
    subtotal = Column(Float, nullable=False)
    impuestos = Column(Float, default=0.0, nullable=False)
    descuentos = Column(Float, default=0.0, nullable=False)
    total = Column(Float, nullable=False)
    
    # Timestamps
    fecha_emision = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reserva = relationship("Reserva", back_populates="factura")
    pagos = relationship("Pago", back_populates="factura")
    
    def __repr__(self):
        return f"<Factura {self.numero_factura} - Total: ${self.total}>"
