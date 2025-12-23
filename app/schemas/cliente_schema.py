"""
Schemas para Cliente
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    """Base de Cliente"""
    nombre: str
    apellido: str
    identificacion: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Schema para crear cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Schema para actualizar cliente"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema de respuesta de cliente"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
