"""
Schemas para Transacción
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime


class TransaccionBase(BaseModel):
    """Base de Transacción"""
    cuenta_id: int
    tipo: str  # ingreso, egreso
    concepto: str
    descripcion: Optional[str] = None
    monto: float
    fecha_transaccion: date
    referencia: Optional[str] = None
    
    @validator('monto')
    def validar_monto(cls, monto):
        if monto == 0:
            raise ValueError('El monto no puede ser cero')
        return monto


class TransaccionCreate(TransaccionBase):
    """Schema para crear transacción"""
    pass


class TransaccionResponse(TransaccionBase):
    """Schema de respuesta de transacción"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class LibroDiarioQuery(BaseModel):
    """Query para libro diario"""
    fecha_inicio: date
    fecha_fin: date
