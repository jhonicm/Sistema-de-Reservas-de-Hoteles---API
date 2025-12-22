"""
Modelo de Usuario
@Entity
@Table
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from app.config.database import Base


class Usuario(Base):
    """
    Entidad Usuario - Gestión de usuarios del sistema
    Roles: Administrador, Recepcionista, Contador, Gerencia
    """
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    nombre = Column(String)  # <-- Agregado
    apellido = Column(String)  # <-- Agregado
    email = Column(String, unique=True, index=True)  # <-- Agregado
    hashed_password = Column(String)  # <-- Este campo es obligatorio
    
    # Rol del usuario
    rol = Column(String)  # Administrador, Recepcionista, Contador, Gerencia
    
    # Estado
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # <-- Agregado
    
    def __repr__(self):
        return f"<Usuario {self.username} - {self.rol}>"
