"""
Controlador de Facturas
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.config.security import require_role
from app.services.factura_service import factura_service
from app.schemas.factura_schema import FacturaCreate, FacturaResponse, FacturaUpdate  # Agrega FacturaUpdate
from app.schemas.common import ResponseData, ResponseList

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.post(
    "/facturas",
)
def create_factura(
    factura_data: FacturaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Contador"]))
):
    """
    Crear nueva factura manualmente
    """
    factura = factura_service.create(db, factura_data)
    return ResponseData(
        success=True,
        message="Factura creada correctamente",
        data=factura
    )


@router.get(
    "/facturas",
)
def get_facturas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener todas las facturas
    """
    facturas = factura_service.get_all(db, skip, limit)
    return ResponseList(
        success=True,
        message="Facturas obtenidas correctamente",
        data=facturas,
        total=len(facturas)
    )


@router.get(
    "/facturas/{factura_id}",
)
def get_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener factura por ID
    """
    factura = factura_service.get_by_id(db, factura_id)
    return ResponseData(
        success=True,
        message="Factura obtenida correctamente",
        data=factura
    )


@router.put(
    "/facturas/{factura_id}",
)
def update_factura(factura_id: int, factura: FacturaUpdate, db: Session = Depends(get_db)):
    """
    Actualizar una factura existente
    """
    factura_actualizada = factura_service.update(db, factura_id, factura)
    return ResponseData(
        success=True,
        message="Factura actualizada correctamente",
        data=factura_actualizada
    )


@router.delete(
    "/facturas/{factura_id}",
)
def delete_factura(factura_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una factura del sistema
    """
    factura_service.delete(db, factura_id)
    return ResponseData(
        success=True,
        message="Factura eliminada correctamente",
        data=None
    )
