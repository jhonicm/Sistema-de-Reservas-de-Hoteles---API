"""
Controlador de Clientes
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config.database import get_db
from app.config.security import require_role
from app.services.cliente_service import cliente_service
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse
from app.schemas.common import ResponseData, ResponseList

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post(
    "/clientes",
)
def create_cliente(
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista"]))
):
    """
    Crear nuevo cliente
    """
    cliente = cliente_service.create(db, cliente_data)
    return ResponseData(
        success=True,
        message="Cliente creado correctamente",
        data=cliente
    )


@router.get(
    "/clientes",
)
def get_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Gerencia"]))
):
    """
    Obtener todos los clientes
    """
    clientes = cliente_service.get_all(db, skip, limit)
    return ResponseList(
        success=True,
        message="Clientes obtenidos correctamente",
        data=clientes,
        total=len(clientes)
    )


@router.get(
    "/clientes/{cliente_id}",
)
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Gerencia"]))
):
    """
    Obtener cliente por ID
    """
    cliente = cliente_service.get_by_id(db, cliente_id)
    return ResponseData(
        success=True,
        message="Cliente obtenido correctamente",
        data=cliente
    )


@router.put(
    "/clientes/{cliente_id}",
)
def update_cliente(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista"]))
):
    """
    Actualizar cliente
    """
    cliente = cliente_service.update(db, cliente_id, cliente_data)
    return ResponseData(
        success=True,
        message="Cliente actualizado correctamente",
        data=cliente
    )


@router.delete(
    "/clientes/{cliente_id}",
)
def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Eliminar cliente (solo si no tiene reservas activas)
    """
    cliente_service.delete(db, cliente_id)
    return ResponseData(
        success=True,
        message="Cliente eliminado correctamente",
        data={"deleted": True}
    )
