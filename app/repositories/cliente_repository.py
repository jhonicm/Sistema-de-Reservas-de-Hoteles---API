"""
Repositorio de Clientes
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):
    """
    Repositorio para la entidad Cliente
    """
    
    def __init__(self):
        super().__init__(Cliente)
    
    def get_by_identificacion(self, db: Session, identificacion: str) -> Optional[Cliente]:
        """Buscar cliente por identificación"""
        return db.query(Cliente).filter(Cliente.identificacion == identificacion).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Cliente]:
        """Buscar cliente por email"""
        return db.query(Cliente).filter(Cliente.email == email).first()
    
    def search(self, db: Session, query: str) -> list[Cliente]:
        """Buscar clientes por nombre, apellido, identificación o email"""
        search_pattern = f"%{query}%"
        return db.query(Cliente).filter(
            (Cliente.nombre.like(search_pattern)) |
            (Cliente.apellido.like(search_pattern)) |
            (Cliente.identificacion.like(search_pattern)) |
            (Cliente.email.like(search_pattern))
        ).all()


# Instancia singleton
cliente_repository = ClienteRepository()
