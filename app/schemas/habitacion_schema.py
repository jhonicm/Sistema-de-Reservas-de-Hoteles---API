"""
Schemas para Habitación
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HabitacionBase(BaseModel):
    """Base de Habitación"""
    numero: str
    tipo: str
    precio_noche: float
    capacidad: int
    caracteristicas: Optional[str] = None


class HabitacionCreate(HabitacionBase):
    """Schema para crear habitación"""
    pass


class HabitacionUpdate(BaseModel):
    """Schema para actualizar habitación"""
    tipo: Optional[str] = None
    precio_noche: Optional[float] = None
    capacidad: Optional[int] = None
    caracteristicas: Optional[str] = None
    estado: Optional[str] = None
    activa: Optional[bool] = None


class HabitacionResponse(HabitacionBase):
    """Schema de respuesta de habitación"""
    id: int
    estado: str
    activa: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class HabitacionDisponibleQuery(BaseModel):
    """Query para buscar habitaciones disponibles"""
    fecha_entrada: str  # YYYY-MM-DD
    fecha_salida: str  # YYYY-MM-DD
    tipo: Optional[str] = None
