"""
Modelo de Transacción Contable
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Transaccion(Base):
    """
    Entidad Transacción - Movimientos contables (ingresos/egresos)
    """
    __tablename__ = "transacciones"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Relación con cuenta contable
    cuenta_id = Column(Integer, ForeignKey("cuentas_contables.id"), nullable=False)
    
    # Información de la transacción
    tipo = Column(String(20), nullable=False)  # ingreso, egreso
    concepto = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    # Monto
    monto = Column(Float, nullable=False)
    
    # Fecha de la transacción
    fecha_transaccion = Column(Date, nullable=False)
    
    # Referencia (puede ser ID de factura, pago, etc.)
    referencia = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    cuenta = relationship("CuentaContable", back_populates="transacciones")
    
    # Restricciones
    __table_args__ = (
        CheckConstraint('monto != 0', name='check_monto_no_cero'),
    )
    
    def __repr__(self):
        return f"<Transaccion #{self.id} - {self.tipo} - ${self.monto} - {self.concepto}>"
