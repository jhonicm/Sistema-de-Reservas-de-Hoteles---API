"""
Servicio de Clientes
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.repositories.cliente_repository import cliente_repository
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse


class ClienteService:
    """
    Servicio de gestión de clientes
    """
    
    def create(self, db: Session, cliente_data: ClienteCreate) -> ClienteResponse:
        """
        Crear nuevo cliente
        """
        # Verificar identificación única
        if cliente_repository.get_by_identificacion(db, cliente_data.identificacion):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un cliente con esta identificación"
            )
        
        # Verificar email único si se proporciona
        if cliente_data.email:
            if cliente_repository.get_by_email(db, cliente_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
        
        # Crear cliente
        cliente = cliente_repository.create(db, cliente_data.model_dump())
        return ClienteResponse.model_validate(cliente)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ClienteResponse]:
        """
        Obtener todos los clientes
        """
        clientes = cliente_repository.get_all(db, skip, limit)
        return [ClienteResponse.model_validate(c) for c in clientes]
    
    def get_by_id(self, db: Session, cliente_id: int) -> ClienteResponse:
        """
        Obtener cliente por ID
        """
        cliente = cliente_repository.get_by_id(db, cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        return ClienteResponse.model_validate(cliente)
    
    def search(self, db: Session, query: str) -> List[ClienteResponse]:
        """
        Buscar clientes por nombre, apellido o identificación
        """
        clientes = cliente_repository.search(db, query)
        return [ClienteResponse.model_validate(c) for c in clientes]
    
    def update(
        self,
        db: Session,
        cliente_id: int,
        cliente_data: ClienteUpdate
    ) -> ClienteResponse:
        """
        Actualizar cliente
        """
        # Verificar que existe
        cliente = cliente_repository.get_by_id(db, cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Verificar email único si se está cambiando
        if cliente_data.email:
            existing = cliente_repository.get_by_email(db, cliente_data.email)
            if existing and existing.id != cliente_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
        
        # Actualizar
        update_data = cliente_data.model_dump(exclude_unset=True)
        updated_cliente = cliente_repository.update(db, cliente_id, update_data)
        return ClienteResponse.model_validate(updated_cliente)
    
    def delete(self, db: Session, cliente_id: int) -> bool:
        """
        Eliminar cliente
        """
        cliente = cliente_repository.get_by_id(db, cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Verificar que no tenga reservas activas
        if cliente.reservas:
            reservas_activas = [r for r in cliente.reservas if r.estado != "Cancelada"]
            if reservas_activas:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede eliminar un cliente con reservas activas"
                )
        
        # Eliminar
        cliente_repository.delete(db, cliente_id)
        return True


# Instancia singleton
cliente_service = ClienteService()
