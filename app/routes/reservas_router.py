"""
Controlador de Reservas
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.config.security import require_role
from app.services.reserva_service import reserva_service
from app.schemas.reserva_schema import ReservaCreate, ReservaUpdate, ReservaResponse
from app.schemas.common import ResponseData, ResponseList

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "/reservas",
)
def create_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista"]))
):
    """
    Crear nueva reserva
    """
    reserva = reserva_service.create(db, reserva_data)
    return ResponseData(
        success=True,
        message="Reserva creada correctamente",
        data=reserva
    )


@router.get(
    "/reservas",
)
def get_reservas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Gerencia"]))
):
    """
    Obtener todas las reservas
    """
    reservas = reserva_service.get_all(db, skip, limit)
    return ResponseList(
        success=True,
        message="Reservas obtenidas correctamente",
        data=reservas,
        total=len(reservas)
    )


@router.get(
    "/reservas/{reserva_id}",
)
def get_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Gerencia"]))
):
    """
    Obtener reserva por ID
    """
    reserva = reserva_service.get_by_id(db, reserva_id)
    return ResponseData(
        success=True,
        message="Reserva obtenida correctamente",
        data=reserva
    )


@router.put(
    "/reservas/{reserva_id}",
)
def update_reserva(reserva_id: int, reserva: ReservaUpdate, db: Session = Depends(get_db)):
    """
    Actualizar una reserva existente
    """
    reserva_actualizada = reserva_service.update(db, reserva_id, reserva)
    return ResponseData(
        success=True,
        message="Reserva actualizada correctamente",
        data=reserva_actualizada
    )


@router.delete(
    "/reservas/{reserva_id}",
)
def cancel_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """
    Cancelar una reserva existente
    """
    reserva_service.cancelar(db, reserva_id)
    return ResponseData(
        success=True,
        message="Reserva cancelada correctamente",
        data=None
    )
