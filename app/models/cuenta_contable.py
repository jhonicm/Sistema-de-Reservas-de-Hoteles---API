"""
Modelo de Cuenta Contable
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class CuentaContable(Base):
    """
    Entidad CuentaContable - Plan de cuentas contable jerárquico
    """
    __tablename__ = "cuentas_contables"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Código único de cuenta
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    
    # Jerarquía
    cuenta_padre_id = Column(Integer, ForeignKey("cuentas_contables.id"), nullable=True)
    
    # Tipo de cuenta
    tipo = Column(String(20), nullable=False)  # activo, pasivo, ingreso, egreso
    
    # Estado
    activa = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    cuenta_padre = relationship("CuentaContable", remote_side=[id], backref="subcuentas")
    transacciones = relationship("Transaccion", back_populates="cuenta")
    
    def __repr__(self):
        return f"<CuentaContable {self.codigo} - {self.nombre}>"
