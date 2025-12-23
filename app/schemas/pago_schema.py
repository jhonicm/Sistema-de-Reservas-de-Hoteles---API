"""
Schemas para Pago
"""

from pydantic import BaseModel, validator
from datetime import datetime


class PagoBase(BaseModel):
    """Base de Pago"""
    factura_id: int
    monto: float
    metodo_pago: str  # efectivo, tarjeta, transferencia
    referencia: str | None = None
    
    @validator('monto')
    def validar_monto(cls, monto):
        if monto <= 0:
            raise ValueError('El monto debe ser mayor a 0')
        return monto


class PagoCreate(PagoBase):
    """Schema para crear pago"""
    pass


class PagoResponse(PagoBase):
    """Schema de respuesta de pago"""
    id: int
    fecha_pago: datetime
    
    class Config:
        from_attributes = True
