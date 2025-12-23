"""
Schemas para Reserva
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime


class ReservaBase(BaseModel):
    """Base de Reserva"""
    cliente_id: int
    habitacion_id: int
    fecha_entrada: date
    fecha_salida: date
    observaciones: Optional[str] = None
    
    @validator('fecha_salida')
    def validar_fechas(cls, fecha_salida, values):
        if 'fecha_entrada' in values and fecha_salida <= values['fecha_entrada']:
            raise ValueError('La fecha de salida debe ser posterior a la fecha de entrada')
        return fecha_salida


class ReservaCreate(ReservaBase):
    """Schema para crear reserva"""
    pass


class ReservaUpdate(BaseModel):
    """Schema para actualizar reserva"""
    fecha_entrada: Optional[date] = None
    fecha_salida: Optional[date] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    
    @validator('fecha_salida')
    def validar_fechas(cls, fecha_salida, values):
        if 'fecha_entrada' in values and fecha_salida and values['fecha_entrada']:
            if fecha_salida <= values['fecha_entrada']:
                raise ValueError('La fecha de salida debe ser posterior a la fecha de entrada')
        return fecha_salida


class ReservaResponse(ReservaBase):
    """Schema de respuesta de reserva"""
    id: int
    precio_total: float
    estado: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReservaCancelRequest(BaseModel):
    """Request para cancelar reserva"""
    motivo: Optional[str] = None
