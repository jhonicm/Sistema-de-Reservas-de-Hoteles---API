"""
Controlador de Contabilidad
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.config.database import get_db
from app.config.security import require_role
from app.services.contabilidad_service import contabilidad_service
from app.schemas.cuenta_contable_schema import (
    CuentaContableCreate,
    CuentaContableUpdate,
    CuentaContableResponse
)
from app.schemas.transaccion_schema import TransaccionCreate, TransaccionResponse
from app.schemas.common import ResponseData, ResponseList

router = APIRouter(prefix="/contabilidad", tags=["Contabilidad"])


# ========== Cuentas Contables ==========

@router.post("/cuentas", response_model=ResponseData[CuentaContableResponse])
def create_cuenta(
    cuenta_data: CuentaContableCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador"]))
):
    """
    Crear nueva cuenta contable
    """
    cuenta = contabilidad_service.create_cuenta(db, cuenta_data)
    return ResponseData(
        success=True,
        message="Cuenta contable creada correctamente",
        data=cuenta
    )


@router.get("/cuentas", response_model=ResponseList[CuentaContableResponse])
def get_cuentas(
    tipo: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener cuentas contables
    """
    cuentas = contabilidad_service.get_cuentas(db, tipo, skip, limit)
    return ResponseList(
        success=True,
        message="Cuentas obtenidas correctamente",
        data=cuentas,
        total=len(cuentas)
    )


@router.get("/cuentas/{cuenta_id}", response_model=ResponseData[CuentaContableResponse])
def get_cuenta(
    cuenta_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener cuenta por ID
    """
    cuenta = contabilidad_service.get_cuenta_by_id(db, cuenta_id)
    return ResponseData(
        success=True,
        message="Cuenta obtenida correctamente",
        data=cuenta
    )


@router.put("/cuentas/{cuenta_id}", response_model=ResponseData[CuentaContableResponse])
def update_cuenta(
    cuenta_id: int,
    cuenta_data: CuentaContableUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador"]))
):
    """
    Actualizar cuenta contable
    """
    cuenta = contabilidad_service.update_cuenta(db, cuenta_id, cuenta_data)
    return ResponseData(
        success=True,
        message="Cuenta actualizada correctamente",
        data=cuenta
    )


# ========== Transacciones ==========

@router.post("/transacciones", response_model=ResponseData[TransaccionResponse])
def create_transaccion(
    transaccion_data: TransaccionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador"]))
):
    """
    Registrar nueva transacción contable
    """
    transaccion = contabilidad_service.create_transaccion(db, transaccion_data)
    return ResponseData(
        success=True,
        message="Transacción registrada correctamente",
        data=transaccion
    )


@router.get("/transacciones", response_model=ResponseList[TransaccionResponse])
def get_transacciones(
    cuenta_id: Optional[int] = Query(None),
    fecha_desde: Optional[date] = Query(None),
    fecha_hasta: Optional[date] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener transacciones contables
    """
    transacciones = contabilidad_service.get_transacciones(
        db,
        cuenta_id,
        fecha_desde,
        fecha_hasta,
        skip,
        limit
    )
    return ResponseList(
        success=True,
        message="Transacciones obtenidas correctamente",
        data=transacciones,
        total=len(transacciones)
    )


@router.get("/balance", response_model=ResponseData[dict])
def get_balance(
    fecha_desde: Optional[date] = Query(None),
    fecha_hasta: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Obtener balance general
    """
    balance = contabilidad_service.get_balance(db, fecha_desde, fecha_hasta)
    return ResponseData(
        success=True,
        message="Balance obtenido correctamente",
        data=balance
    )
