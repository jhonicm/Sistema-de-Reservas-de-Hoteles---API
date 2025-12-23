"""
Schemas para Cuenta Contable
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CuentaContableBase(BaseModel):
    """Base de Cuenta Contable"""
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    tipo: str  # activo, pasivo, ingreso, egreso
    cuenta_padre_id: Optional[int] = None


class CuentaContableCreate(CuentaContableBase):
    """Schema para crear cuenta contable"""
    pass


class CuentaContableUpdate(BaseModel):
    """Schema para actualizar cuenta contable"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activa: Optional[bool] = None


class CuentaContableResponse(CuentaContableBase):
    """Schema de respuesta de cuenta contable"""
    id: int
    activa: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
