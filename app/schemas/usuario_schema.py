"""
Schemas para Usuario
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    """Base de Usuario"""
    username: str
    email: EmailStr
    nombre: str
    apellido: str
    rol: str  # Administrador, Recepcionista, Contador, Gerencia


class UsuarioCreate(UsuarioBase):
    """Schema para crear usuario"""
    password: str


class UsuarioUpdate(BaseModel):
    """Schema para actualizar usuario"""
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    """Schema de respuesta de usuario"""
    id: int
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
