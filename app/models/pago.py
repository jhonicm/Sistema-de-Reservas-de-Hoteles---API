"""
Modelo de Pago
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Pago(Base):
    """
    Entidad Pago - Registro de pagos de facturas
    """
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Relación con factura
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    
    # Información del pago
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=False)  # efectivo, tarjeta, transferencia
    referencia = Column(String(100), nullable=True)
    
    # Timestamps
    fecha_pago = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    factura = relationship("Factura", back_populates="pagos")
    
    # Restricciones
    __table_args__ = (
        CheckConstraint('monto > 0', name='check_monto_positivo'),
    )
    
    def __repr__(self):
        return f"<Pago #{self.id} - Factura:{self.factura_id} - ${self.monto} - {self.metodo_pago}>"
