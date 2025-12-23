"""
Esquemas para la validación de datos de las facturas
"""

from pydantic import BaseModel
from typing import List, Optional

class FacturaBase(BaseModel):
    """Schema base para una factura"""
    servicios_adicionales: List[str]
    descuento: float
    estado: str


class FacturaCreate(FacturaBase):
    """Schema para crear una nueva factura"""
    pass


class FacturaUpdate(BaseModel):
    """Schema para actualizar una factura"""
    servicios_adicionales: Optional[List[str]] = None
    descuento: Optional[float] = None
    estado: Optional[str] = None
    
    class Config:
        from_attributes = True


class Factura(FacturaBase):
    """Schema para una factura existente"""
    id: int

    class Config:
        orm_mode = True