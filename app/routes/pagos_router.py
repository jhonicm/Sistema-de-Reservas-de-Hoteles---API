"""
Controlador de Pagos
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.config.security import require_role
from app.services.pago_service import pago_service
from app.schemas.pago_schema import PagoCreate, PagoResponse
from app.schemas.common import ResponseData, ResponseList

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.post("", response_model=ResponseData[PagoResponse])
def create_pago(
    pago_data: PagoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Contador"]))
):
    """
    Registrar nuevo pago
    """
    pago = pago_service.create(db, pago_data)
    return ResponseData(
        success=True,
        message="Pago registrado correctamente",
        data=pago
    )


@router.get("", response_model=ResponseList[PagoResponse])
def get_pagos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener todos los pagos
    """
    pagos = pago_service.get_all(db, skip, limit)
    return ResponseList(
        success=True,
        message="Pagos obtenidos correctamente",
        data=pagos,
        total=len(pagos)
    )


@router.get("/factura/{factura_id}", response_model=ResponseList[PagoResponse])
def get_pagos_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener todos los pagos de una factura específica
    """
    pagos = pago_service.get_by_factura(db, factura_id)
    return ResponseList(
        success=True,
        message="Pagos de la factura obtenidos",
        data=pagos,
        total=len(pagos)
    )


@router.get("/factura/{factura_id}/saldo", response_model=ResponseData[dict])
def get_saldo_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Recepcionista"]))
):
    """
    Obtener saldo pendiente de una factura
    """
    saldo = pago_service.get_saldo_pendiente(db, factura_id)
    return ResponseData(
        success=True,
        message="Saldo obtenido correctamente",
        data={"saldo_pendiente": float(saldo)}
    )


@router.get("/{pago_id}", response_model=ResponseData[PagoResponse])
def get_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener pago por ID
    """
    pago = pago_service.get_by_id(db, pago_id)
    return ResponseData(
        success=True,
        message="Pago obtenido correctamente",
        data=pago
    )
